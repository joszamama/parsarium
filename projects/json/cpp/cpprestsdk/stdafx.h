// Parsarium build shim: replaces cpprest's Release/src/pch/stdafx.h, which pulls in the
// HTTP, websocket, OAuth, and Boost.Asio headers. Only the headers the JSON and UTF
// conversion translation units need are included; no cpprest source file is changed.
#pragma once
#define __STDC_LIMIT_MACROS
#include <algorithm>
#include <array>
#include <assert.h>
#include <atomic>
#include <cstdint>
#include <cstring>
#include <exception>
#include <memory>
#include <mutex>
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include "cpprest/details/basic_types.h"
#include "cpprest/details/cpprest_compat.h"
#include "cpprest/version.h"
#include "cpprest/json.h"
#include "cpprest/asyncrt_utils.h"
