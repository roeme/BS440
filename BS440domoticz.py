'''
BS440domoticz.py
Update weight value to Domoticz home automation system
'''
import urllib2
import base64
import logging


def UpdateDomoticz(config, weightdata):
    log = logging.getLogger(__name__)
    domoticzurl = config.get('Domoticz', 'domoticz_url')
    personsection = 'Person' + str(weightdata[0]['person'])
    if config.has_section(personsection):
        domoticzid = config.get(personsection, 'domoticz_id')
        scaleuser = config.get(personsection, 'username')
        domoticzhid = config.get(personsection, 'domoticz_hid')
        domoticzdunit = config.get(personsection, 'domoticz_dunit')
    else:
        log.error('Unable to update Domoticz: No details found in ini file '
                  'for person %d' % (weightdata[0]['person']))
        return
    try:
        log.info('Updating Domoticz for user %s at index %s with weight %s' % (
                  scaleuser, domoticzid, weightdata[0]['weight']))
        url = 'http://%s/json.htm?type=command&param=udevice&hid=%s&' \
              'did=%s&dunit=%s&dtype=93&dsubtype=1&nvalue=0&svalue=%s' % (
               domoticzurl, domoticzhid, domoticzid, domoticzdunit, 
               weightdata[0]['weight'])
        log.debug('calling url: %s' % (url))
        req = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (
                       domoticzuser, domoticzpwd)).replace('\n', '')
        req.add_header('Authorization', 'Basic %s' % base64string)
        resp = urllib2.urlopen(req)
        log.info('Domoticz succesfully updated')
    except:
        log.error('Unable to update Domoticz: Error sending data.')