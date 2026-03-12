# -*- coding: utf-8 -*-
import settings
base_api_url = "/{}/deploy/api/deploy/esb/v0_1/".format(getattr(settings, "BK_ENV", "o"))
