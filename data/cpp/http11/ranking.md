# C++ × HTTP/1.1: verified parser ranking

2 verified third-party package paths; working goal 20, ceiling 30. GitHub stars of each primary upstream repository were observed on 2026-11-12. They proxy broad project interest, not HTTP-specific adoption, and are compared only within C++. The saved Conan Center recipe-name hits are alphabetic discovery leads, not a ranking. Eight plausible leads remain unresolved, so this is not a complete most-used selection.

| Rank | Package | Pinned release | Repository stars | Local input API | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [Poco.Net](https://docs.pocoproject.org/current/Poco.Net.HTTPRequest.html) | 1.15.4 | 9,498 | `HTTPRequest::read(std::istream&)` | Poco.Net HTTPRequest parser |
| 2 | [Boost.Beast](https://www.boost.org/latest/libs/beast/doc/html/beast/ref/boost__beast__http__basic_parser/put.html) | 1.92.0 | 4,833 | `request_parser::put(local buffer, error_code&)` | Boost.Beast native HTTP parser |

Both passed the valid request control. See `parsers.json` for exact output and `verification.json` for the build and run commands. Search leads and the standard-library inventory are recorded separately.
