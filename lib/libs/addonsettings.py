import xbmc

from lib.libs import pykodi
try:
    import projectkeys
except ImportError:
    projectkeys = None

addon = pykodi.get_main_addon()

DEFAULT_IMAGESIZE = '1'
AVAILABLE_IMAGESIZES = {'0': (10000, 10000, 600), '1': (1920, 1080, 600), '2': (1280, 720, 480)}

PROGRESS_DISPLAY_FULLPROGRESS = '0'
PROGRESS_DISPLAY_WARNINGSERRORS = '1'
PROGRESS_DISPLAY_NONE = '2' # Only add-on crashes

class Settings(object):
    def __init__(self):
        self.addon_path = addon.path
        self.datapath = addon.datapath
        self._autoadd_episodes = ()
        self.update_settings()
        self.update_useragent()

    def update_useragent(self):
        beefversion = pykodi.get_main_addon().version
        if pykodi.get_kodi_version() < 17:
            from lib.libs import quickjson
            props = quickjson.get_application_properties(['name', 'version'])
            appversion = '{0}.{1}'.format(props['version']['major'], props['version']['minor'])
            self.useragent = 'ArtworkBeef/{0} {1}/{2}'.format(beefversion, props['name'], appversion)
            return
        self.useragent = 'ArtworkBeef/{0} '.format(beefversion) + xbmc.getUserAgent()

    def update_settings(self):
        self._autoadd_episodes = addon.get_setting('autoaddepisodes_list') if addon.get_setting('episode.fanart') else ()
        self.enableservice = addon.get_setting('enableservice')
        self.enableservice_music = addon.get_setting('enableservice_music')
        self.enable_olditem_updates = addon.get_setting('enable_olditem_updates')
        self.titlefree_fanart = addon.get_setting('titlefree_fanart')
        self.titlefree_poster = addon.get_setting('titlefree_poster')
        self.setartwork_fromparent = addon.get_setting('setartwork_fromparent')
        self.identify_alternatives = addon.get_setting('identify_alternatives')
        self.report_peritem = addon.get_setting('report_peritem')
        self.fanarttv_clientkey = addon.get_setting('fanarttv_key')
        self.default_tvidsource = addon.get_setting('default_tvidsource')
        self.progressdisplay = addon.get_setting('progress_display')
        self.final_notification = addon.get_setting('final_notification')
        self.save_extrafanart = addon.get_setting('save_extrafanart')
        self.save_extrafanart_mvids = addon.get_setting('save_extrafanart_mvids')
        self.remove_deselected_files = addon.get_setting('remove_deselected_files')
        self.recycle_removed = addon.get_setting('recycle_removed')
        self.savewith_basefilename = addon.get_setting('savewith_basefilename')
        self.savewith_basefilename_mvids = addon.get_setting('savewith_basefilename_mvids')
        self.albumartwithmediafiles = addon.get_setting('albumartwithmediafiles')
        self.cache_local_video_artwork = addon.get_setting('cache_local_video_artwork')
        self.cache_local_music_artwork = addon.get_setting('cache_local_music_artwork')

        self.language_override = addon.get_setting('language_override')
        if self.language_override == 'None':
            self.language_override = None

        try:
            self.minimum_rating = int(addon.get_setting('minimum_rating'))
        except ValueError:
            self.minimum_rating = 5
            addon.set_setting('minimum_rating', "5")

        sizesetting = addon.get_setting('preferredsize')
        if sizesetting not in AVAILABLE_IMAGESIZES:
            sizesetting = DEFAULT_IMAGESIZE
            addon.set_setting('preferredsize', DEFAULT_IMAGESIZE)
        self.preferredsize = AVAILABLE_IMAGESIZES[sizesetting][0:2]
        self.minimum_size = AVAILABLE_IMAGESIZES[sizesetting][2]

        self.fanarttv_apikey = addon.get_setting('apikey.fanarttv')
        self.tvdb_apikey = addon.get_setting('apikey.tvdb')
        self.tmdb_apikey = addon.get_setting('apikey.tmdb')
        self.tadb_apikey = addon.get_setting('apikey.tadb')
        if projectkeys:
            if not self.fanarttv_apikey:
                self.fanarttv_apikey = projectkeys.FANARTTV_PROJECTKEY
            if not self.tvdb_apikey:
                self.tvdb_apikey = projectkeys.THETVDB_PROJECTKEY
            if not self.tmdb_apikey:
                self.tmdb_apikey = projectkeys.TMDB_PROJECTKEY
            if not self.tadb_apikey:
                self.tadb_apikey = projectkeys.TADB_PROJECTKEY

        pykodi.set_log_scrubstring('fanarttv-client-apikey', self.fanarttv_clientkey)
        pykodi.set_log_scrubstring('fanarttv-apikey', self.fanarttv_apikey)
        pykodi.set_log_scrubstring('theaudiodb-apikey', self.tadb_apikey)
        pykodi.set_log_scrubstring('themoviedb-apikey', self.tmdb_apikey)
        pykodi.set_log_scrubstring('thetvdbv-apikey', self.tvdb_apikey)

    @property
    def autoadd_episodes(self):
        return self._autoadd_episodes

    @autoadd_episodes.setter
    def autoadd_episodes(self, value):
        self._autoadd_episodes = value
        addon.set_setting('autoaddepisodes_list', value)

settings = Settings()
