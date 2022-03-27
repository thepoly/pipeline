from django.template.loader import render_to_string

from debug_toolbar import settings as dt_settings
from debug_toolbar.utils import get_name_from_obj


class Panel:
    """
    Base class for panels.
    """

    def __init__(self, toolbar, get_response):
        self.toolbar = toolbar
        self.get_response = get_response

    # Private panel properties

    @property
    def panel_id(self):
        return self.__class__.__name__

    @property
    def enabled(self):
        # Check to see if settings has a default value for it
        disabled_panels = dt_settings.get_config()["DISABLE_PANELS"]
        panel_path = get_name_from_obj(self)
        # Some panels such as the SQLPanel and TemplatesPanel exist in a
        # panel module, but can be disabled without panel in the path.
        # For that reason, replace .panel. in the path and check for that
        # value in the disabled panels as well.
        disable_panel = (
            panel_path in disabled_panels
            or panel_path.replace(".panel.", ".") in disabled_panels
        )
        if disable_panel:
            default = "off"
        else:
            default = "on"
        # The user's cookies should override the default value
        return self.toolbar.request.COOKIES.get("djdt" + self.panel_id, default) == "on"

    # Titles and content

    @property
    def nav_title(self):
        """
        Title shown in the side bar. Defaults to :attr:`title`.
        """
        return self.title

    @property
    def nav_subtitle(self):
        """
        Subtitle shown in the side bar. Defaults to the empty string.
        """
        return ""

    @property
    def has_content(self):
        """
        ``True`` if the panel can be displayed in full screen, ``False`` if
        it's only shown in the side bar. Defaults to ``True``.
        """
        return True

    @property
    def title(self):
        """
        Title shown in the panel when it's displayed in full screen.

        Mandatory, unless the panel sets :attr:`has_content` to ``False``.
        """
        raise NotImplementedError

    @property
    def template(self):
        """
        Template used to render :attr:`content`.

        Mandatory, unless the panel sets :attr:`has_content` to ``False`` or
        overrides `attr`:content`.
        """
        raise NotImplementedError

    @property
    def content(self):
        """
        Content of the panel when it's displayed in full screen.

        By default this renders the template defined by :attr:`template`.
        Statistics stored with :meth:`record_stats` are available in the
        template's context.
        """
        if self.has_content:
            return render_to_string(self.template, self.get_stats())

    # URLs for panel-specific views

    @classmethod
    def get_urls(cls):
        """
        Return URLpatterns, if the panel has its own views.
        """
        return []

    # Enable and disable (expensive) instrumentation, must be idempotent

    def enable_instrumentation(self):
        """
        Enable instrumentation to gather data for this panel.

        This usually means monkey-patching (!) or registering signal
        receivers. Any instrumentation with a non-negligible effect on
        performance should be installed by this method rather than at import
        time.

        Unless the toolbar or this panel is disabled, this method will be
        called early in :class:`DebugToolbarMiddleware.process_request`. It
        should be idempotent.
        """

    def disable_instrumentation(self):
        """
        Disable instrumentation to gather data for this panel.

        This is the opposite of :meth:`enable_instrumentation`.

        Unless the toolbar or this panel is disabled, this method will be
        called late in the middleware. It should be idempotent.
        """

    # Store and retrieve stats (shared between panels for no good reason)

    def record_stats(self, stats):
        """
        Store data gathered by the panel. ``stats`` is a :class:`dict`.

        Each call to ``record_stats`` updates the statistics dictionary.
        """
        self.toolbar.stats.setdefault(self.panel_id, {}).update(stats)

    def get_stats(self):
        """
        Access data stored by the panel. Returns a :class:`dict`.
        """
        return self.toolbar.stats.get(self.panel_id, {})

    def record_server_timing(self, key, title, value):
        """
        Store data gathered by the panel. ``stats`` is a :class:`dict`.

        Each call to ``record_stats`` updates the statistics dictionary.
        """
        data = {key: {"title": title, "value": value}}
        self.toolbar.server_timing_stats.setdefault(self.panel_id, {}).update(data)

    def get_server_timing_stats(self):
        """
        Access data stored by the panel. Returns a :class:`dict`.
        """
        return self.toolbar.server_timing_stats.get(self.panel_id, {})

    # Standard middleware methods

    def process_request(self, request):
        """
        Like __call__ in Django's middleware.

        Write panel logic related to the request there. Save data with
        :meth:`record_stats`.

        Return the existing response or overwrite it.
        """
        return self.get_response(request)

    def generate_stats(self, request, response):
        """
        Called after :meth:`process_request
        <debug_toolbar.panels.Panel.process_request>`, but may not be executed
        on every request. This will only be called if the toolbar will be
        inserted into the request.

        Write panel logic related to the response there. Post-process data
        gathered while the view executed. Save data with :meth:`record_stats`.

        Does not return a value.
        """

    def generate_server_timing(self, request, response):
        """
        Similar to :meth:`generate_stats
        <debug_toolbar.panels.Panel.generate_stats>`,

        Generate stats for Server Timing https://w3c.github.io/server-timing/

        Does not return a value.
        """