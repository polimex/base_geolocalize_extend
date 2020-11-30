from odoo import fields, models, api, _
from odoo.exceptions import UserError
import requests

import logging

_logger = logging.getLogger(__name__)

########################################
# https://github.com/OCA/partner-contact/blob/11.0/partner_external_map/data/map_website_data.xml
########################################

class GeoCoder(models.AbstractModel):
    """
    Abstract class used to call Geolocalization API and convert addresses
    into GPS coordinates.
    """
    _inherit = "base.geocoder"

    @api.model
    def _get_company_provider(self):
        provider_id = self.env['base.geo_provider'].search(
            [('tech_name', '=', self.env.context.get('map_provider'))])
        if provider_id:
            return provider_id[0]

        provider_id = self.env['base.geo_provider'].search(
            [('tech_name', '=', self.env.company.map_provider_id.tech_name)])
        if provider_id:
            return provider_id[0]

        return super(GeoCoder, self)._get_provider()


    @api.model
    def _get_provider(self):
        return self._get_company_provider()


    @api.model
    def reverse_geo_find(self, lat: float, lon: float):
        provider = self._get_provider().tech_name
        try:
            service = getattr(self, '_call_reverse_' + provider)
            result = service(lat, lon)
        except AttributeError:
            raise UserError(_(
                'Provider %s is not implemented for geolocation service.'
            ) % provider)
        except UserError:
            raise
        except Exception:
            _logger.debug('Reverse geolocalize call failed', exc_info=True)
            result = None
        return result

    @api.model
    def reverse_geo_map(self, lat: float, lon: float):
        provider_count = 0
        if self.env.context.get('map_provider'):
            provider_count = self.env['base.geo_provider'].search_count([('tech_name','=',self.env.context.get('map_provider'))])
        provider = self._get_provider().tech_name if provider_count==0 else self.env.context.get('map_provider')
        try:
            service = getattr(self, '_call_map_' + provider)
            result = service(lat, lon)
        except AttributeError:
            raise UserError(_(
                'Provider %s is not implemented for geolocation service.'
            ) % provider)
        except UserError:
            raise
        except Exception:
            _logger.debug('Reverse geolocalize call failed', exc_info=True)
            result = None
        return result

    @api.model
    def _call_reverse_openstreetmap(self, lat: float, lon: float):
        """
        Use Openstreemap Nominatim service to retrieve address from coordinates
        :return: (latitude, longitude) or None if not found
        """
        if not lat or not lon:
            _logger.info('invalid coordinates given')
            return None
        url = 'https://nominatim.openstreetmap.org/reverse.php'
        try:
            headers = {
                'User-Agent': 'Odoo (http://www.odoo.com/contactus)',
                'Accept-Language': self.env.user.lang
            }
            response = requests.get(url, headers=headers, params={'format': 'jsonv2', 'lon': lon, 'lat': lat, 'zoom': 18})
            _logger.info('openstreetmap nominatim reverse service called')
            if response.status_code != 200:
                _logger.error('Request to openstreetmap reverse service failed.\nCode: %s\nContent: %s' % (response.status_code, response.content))
            result = response.json()
            dn = result['display_name']
        except Exception as e:
            self._raise_query_error(e)
        return dn

    @api.model
    def _call_map_openstreetmap(self, lat: float, lon: float):
        if not lat or not lon:
            _logger.info('invalid coordinates given')
            return None
        url = 'https://www.openstreetmap.org/?zoom=15&amp;mlat={LATITUDE}&amp;mlon={LONGITUDE}'
        return url.format(
            LATITUDE=lat,
            LONGITUDE=lon
        )

    @api.model
    def _call_reverse_googlemap(self, lat, lon):
        provider = self._get_provider().tech_name
        raise UserError(_(
            'Reverse geolocalize with  %s is not implemented yet.'
        ) % provider)

    @api.model
    def _call_map_googlemap(self, lat: float, lon: float):
        if not lat or not lon:
            _logger.info('invalid coordinates given')
            return None
        url = 'https://www.google.com/maps?z=15&amp;q={LATITUDE},{LONGITUDE}'
        return url.format(
            LATITUDE=lat,
            LONGITUDE=lon
        )
