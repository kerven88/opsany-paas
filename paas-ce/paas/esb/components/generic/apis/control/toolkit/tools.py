# -*- coding: utf-8 -*-
import settings
base_api_url = "/{}/control/api/control/esb/v0_1/".format(getattr(settings, "BK_ENV", "o"))
base_execution_api_url = "/{}/control/api/execution/esb/v0_1/".format(getattr(settings, "BK_ENV", "o"))
