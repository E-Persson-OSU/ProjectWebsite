import random
from copy import deepcopy

PROXIES = [
    {
        "_id": "6338e33e2ac8c1a5d6146580",
        "ip": "131.106.216.130",
        "anonymityLevel": "anonymous",
        "asn": "AS6079",
        "city": "Evansville",
        "country": "US",
        "created_at": "2022-10-02T01:02:53.983Z",
        "google": False,
        "isp": "RCN",
        "lastChecked": 1681995983,
        "latency": 114,
        "org": "RCN Corporation",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 929,
        "speed": 524,
        "updated_at": "2023-04-20T13:06:23.052Z",
        "workingPercent": None,
        "upTime": 99.92690058479532,
        "upTimeSuccessCount": 1367,
        "upTimeTryCount": 1368,
    },
    {
        "_id": "633962ad2ac8c1a5d65ff000",
        "ip": "69.75.140.157",
        "anonymityLevel": "anonymous",
        "asn": "AS20001",
        "city": "San Luis",
        "country": "US",
        "created_at": "2022-10-02T10:06:37.637Z",
        "google": False,
        "isp": "Spectrum",
        "lastChecked": 1681995958,
        "latency": 143,
        "org": "Premier Hotels Development",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 1054,
        "speed": 433,
        "updated_at": "2023-04-20T13:05:58.391Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1369,
        "upTimeTryCount": 1369,
    },
    {
        "_id": "631a145c266407aa8c9b5d63",
        "ip": "64.224.255.173",
        "anonymityLevel": "anonymous",
        "asn": "AS395748",
        "city": "New Haven",
        "country": "US",
        "created_at": "2022-09-08T16:12:12.218Z",
        "google": False,
        "isp": "NetSpeed LLC",
        "lastChecked": 1681995918,
        "latency": 77.7,
        "org": "NetSpeed LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 752,
        "speed": 391,
        "updated_at": "2023-04-20T13:05:18.174Z",
        "workingPercent": None,
        "upTime": 99.86111111111111,
        "upTimeSuccessCount": 1438,
        "upTimeTryCount": 1440,
    },
    {
        "_id": "633053782fb0f02dd5f9cfd6",
        "ip": "50.235.149.74",
        "anonymityLevel": "anonymous",
        "asn": "AS7922",
        "city": "Taylor",
        "country": "US",
        "created_at": "2022-09-25T13:11:20.841Z",
        "google": False,
        "isp": "Comcast Cable Communications, LLC",
        "lastChecked": 1681995913,
        "latency": 92.6,
        "org": "Comcast Cable Communications, LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 611,
        "speed": 297,
        "updated_at": "2023-04-20T13:05:13.118Z",
        "workingPercent": None,
        "upTime": 99.78417266187051,
        "upTimeSuccessCount": 1387,
        "upTimeTryCount": 1390,
    },
    {
        "_id": "633bde252ac8c1a5d6cc44d1",
        "ip": "198.229.231.13",
        "anonymityLevel": "anonymous",
        "asn": "AS11062",
        "city": "Spring Valley",
        "country": "US",
        "created_at": "2022-10-04T07:17:57.786Z",
        "google": False,
        "isp": "MTCO Communications",
        "lastChecked": 1681995886,
        "latency": 93,
        "org": "Service Provider Corporation",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 494,
        "speed": 326,
        "updated_at": "2023-04-20T13:04:46.235Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1363,
        "upTimeTryCount": 1363,
    },
    {
        "_id": "633964b22ac8c1a5d66117cd",
        "ip": "198.59.191.234",
        "anonymityLevel": "elite",
        "asn": "AS4181",
        "city": "Carlsbad",
        "country": "US",
        "created_at": "2022-10-02T10:15:14.109Z",
        "google": False,
        "isp": "TDS TELECOM",
        "lastChecked": 1681995848,
        "latency": 151,
        "org": "CHECS",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 479,
        "speed": 502,
        "updated_at": "2023-04-20T13:04:08.291Z",
        "workingPercent": None,
        "upTime": 99.26953981008036,
        "upTimeSuccessCount": 1359,
        "upTimeTryCount": 1369,
    },
    {
        "_id": "6305786ade95dae521871030",
        "ip": "173.219.112.85",
        "anonymityLevel": "anonymous",
        "asn": "AS19108",
        "city": "Sterling",
        "country": "US",
        "created_at": "2022-08-24T01:01:30.567Z",
        "google": False,
        "isp": "Suddenlink Communications",
        "lastChecked": 1681995840,
        "latency": 157,
        "org": "unused",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 528,
        "speed": 615,
        "updated_at": "2023-04-20T13:04:00.102Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1484,
        "upTimeTryCount": 1484,
    },
    {
        "_id": "633bb0fc2ac8c1a5d6b1e1b7",
        "ip": "66.211.155.34",
        "anonymityLevel": "anonymous",
        "asn": "AS10367",
        "city": "Albany",
        "country": "US",
        "created_at": "2022-10-04T04:05:16.868Z",
        "google": False,
        "isp": "FirstLight Fiber",
        "lastChecked": 1681995840,
        "latency": 78.1,
        "org": "First Light Fiber",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 509,
        "speed": 322,
        "updated_at": "2023-04-20T13:04:00.102Z",
        "workingPercent": None,
        "upTime": 98.53264856933237,
        "upTimeSuccessCount": 1343,
        "upTimeTryCount": 1363,
    },
    {
        "_id": "633b0b092ac8c1a5d651f763",
        "ip": "107.178.9.186",
        "anonymityLevel": "anonymous",
        "asn": "AS26077",
        "city": "Dallas",
        "country": "US",
        "created_at": "2022-10-03T16:17:13.162Z",
        "google": False,
        "isp": "Nextlink Broadband",
        "lastChecked": 1681995826,
        "latency": 126,
        "org": "Nextlink Broadband",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 884,
        "speed": 560,
        "updated_at": "2023-04-20T13:03:46.792Z",
        "workingPercent": None,
        "upTime": 96.9208211143695,
        "upTimeSuccessCount": 1322,
        "upTimeTryCount": 1364,
    },
    {
        "_id": "633b5fe52ac8c1a5d682e909",
        "ip": "160.3.168.70",
        "anonymityLevel": "anonymous",
        "asn": "AS11492",
        "city": "Gulfport",
        "country": "US",
        "created_at": "2022-10-03T22:19:17.091Z",
        "google": False,
        "isp": "CABLE ONE, INC.",
        "lastChecked": 1681995826,
        "latency": 125,
        "org": "Sparklight",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 891,
        "speed": 642,
        "updated_at": "2023-04-20T13:03:46.607Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1365,
        "upTimeTryCount": 1365,
    },
    {
        "_id": "633a5fb52ac8c1a5d6f1f697",
        "ip": "69.11.145.106",
        "anonymityLevel": "anonymous",
        "asn": "AS4181",
        "city": "Salome",
        "country": "US",
        "created_at": "2022-10-03T04:06:13.590Z",
        "google": False,
        "isp": "TDS TELECOM",
        "lastChecked": 1681995821,
        "latency": 302,
        "org": "Quail RUN RV Park",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 475,
        "speed": 936,
        "updated_at": "2023-04-20T13:03:41.859Z",
        "workingPercent": None,
        "upTime": 87.99414348462665,
        "upTimeSuccessCount": 1202,
        "upTimeTryCount": 1366,
    },
    {
        "_id": "633a0c192ac8c1a5d6c33f41",
        "ip": "24.116.218.195",
        "anonymityLevel": "anonymous",
        "asn": "AS11492",
        "city": "Pascagoula",
        "country": "US",
        "created_at": "2022-10-02T22:09:29.516Z",
        "google": False,
        "isp": "CABLE ONE, INC.",
        "lastChecked": 1681995817,
        "latency": 157,
        "org": "Sparklight",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 648,
        "speed": 431,
        "updated_at": "2023-04-20T13:03:37.191Z",
        "workingPercent": None,
        "upTime": 98.09941520467837,
        "upTimeSuccessCount": 1342,
        "upTimeTryCount": 1368,
    },
    {
        "_id": "633968532ac8c1a5d66316fc",
        "ip": "50.201.51.216",
        "anonymityLevel": "anonymous",
        "asn": "AS7922",
        "city": "Chesterfield",
        "country": "US",
        "created_at": "2022-10-02T10:30:43.795Z",
        "google": False,
        "isp": "Comcast Cable Communications, LLC",
        "lastChecked": 1681995814,
        "latency": 94.6,
        "org": "Comcast Cable Communications, LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 367,
        "speed": 427,
        "updated_at": "2023-04-20T13:03:34.292Z",
        "workingPercent": None,
        "upTime": 99.12280701754386,
        "upTimeSuccessCount": 1356,
        "upTimeTryCount": 1368,
    },
    {
        "_id": "633b5c542ac8c1a5d680daa0",
        "ip": "70.186.128.126",
        "anonymityLevel": "anonymous",
        "asn": "AS22773",
        "city": "Oklahoma City",
        "country": "US",
        "created_at": "2022-10-03T22:04:04.608Z",
        "google": False,
        "isp": "Cox Communications Inc.",
        "lastChecked": 1681995795,
        "latency": 116,
        "org": "Allegiance Communications, LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 618,
        "speed": 617,
        "updated_at": "2023-04-20T13:03:15.169Z",
        "workingPercent": None,
        "upTime": 99.04692082111437,
        "upTimeSuccessCount": 1351,
        "upTimeTryCount": 1364,
    },
    {
        "_id": "633b86f12ac8c1a5d699bb77",
        "ip": "68.64.250.38",
        "anonymityLevel": "anonymous",
        "asn": "AS46473",
        "city": "Dallas",
        "country": "US",
        "created_at": "2022-10-04T01:05:52.992Z",
        "google": False,
        "isp": "SimpleFiber Communications LLC",
        "lastChecked": 1681995777,
        "latency": 119,
        "org": "SimpleFiber Communications LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 454,
        "speed": 887,
        "updated_at": "2023-04-20T13:02:57.396Z",
        "workingPercent": None,
        "upTime": 97.1386647101981,
        "upTimeSuccessCount": 1324,
        "upTimeTryCount": 1363,
    },
    {
        "_id": "633a5fad2ac8c1a5d6f1f20f",
        "ip": "70.90.138.109",
        "anonymityLevel": "anonymous",
        "asn": "AS7922",
        "city": "Warren",
        "country": "US",
        "created_at": "2022-10-03T04:06:05.301Z",
        "google": False,
        "isp": "Comcast Cable Communications, LLC",
        "lastChecked": 1681995741,
        "latency": 106,
        "org": "Comcast Cable Communications, LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 427,
        "speed": 454,
        "updated_at": "2023-04-20T13:02:21.647Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1366,
        "upTimeTryCount": 1366,
    },
    {
        "_id": "6310075ede95dae521bcfa8d",
        "ip": "198.24.187.91",
        "anonymityLevel": "elite",
        "asn": "AS19437",
        "city": "Ashburn",
        "country": "US",
        "created_at": "2022-09-01T01:14:06.615Z",
        "google": False,
        "isp": "Secured Servers LLC",
        "lastChecked": 1681995736,
        "latency": 82.7,
        "org": "Secured Servers LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 776,
        "speed": 599,
        "updated_at": "2023-04-20T13:02:16.551Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1462,
        "upTimeTryCount": 1462,
    },
    {
        "_id": "631e5dad2fb0f02dd5467351",
        "ip": "207.244.225.39",
        "anonymityLevel": "anonymous",
        "asn": "AS40021",
        "city": "St Louis",
        "country": "US",
        "created_at": "2022-09-11T22:14:05.809Z",
        "google": False,
        "isp": "Contabo Inc.",
        "lastChecked": 1681995725,
        "latency": 97.8,
        "org": "Contabo Inc",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 561,
        "speed": 1992,
        "updated_at": "2023-04-20T13:02:05.995Z",
        "workingPercent": None,
        "upTime": 34.47552447552448,
        "upTimeSuccessCount": 493,
        "upTimeTryCount": 1430,
    },
    {
        "_id": "6332cc9a2fb0f02dd54fb4a9",
        "ip": "74.114.232.162",
        "anonymityLevel": "anonymous",
        "asn": "AS46817",
        "city": "Valparaiso",
        "country": "US",
        "created_at": "2022-09-27T10:12:42.114Z",
        "google": False,
        "isp": "Midwest Telecom of America, Inc",
        "lastChecked": 1681995723,
        "latency": 104,
        "org": "Midwest Telecom of America, Inc",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 993,
        "speed": 557,
        "updated_at": "2023-04-20T13:02:03.539Z",
        "workingPercent": None,
        "upTime": 99.78308026030369,
        "upTimeSuccessCount": 1380,
        "upTimeTryCount": 1383,
    },
    {
        "_id": "633bb0f22ac8c1a5d6b1dcdd",
        "ip": "24.51.32.59",
        "anonymityLevel": "anonymous",
        "asn": "AS13807",
        "city": "Kearney",
        "country": "US",
        "created_at": "2022-10-04T04:05:06.640Z",
        "google": False,
        "isp": "Great Plains Communications LLC",
        "lastChecked": 1681995678,
        "latency": 114,
        "org": "Great Plains Communications LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 969,
        "speed": 400,
        "updated_at": "2023-04-20T13:01:18.487Z",
        "workingPercent": None,
        "upTime": 99.85326485693324,
        "upTimeSuccessCount": 1361,
        "upTimeTryCount": 1363,
    },
    {
        "_id": "633967e72ac8c1a5d662dbc1",
        "ip": "50.236.203.15",
        "anonymityLevel": "anonymous",
        "asn": "AS7922",
        "city": "Peru",
        "country": "US",
        "created_at": "2022-10-02T10:28:55.763Z",
        "google": False,
        "isp": "Comcast Cable Communications, LLC",
        "lastChecked": 1681995672,
        "latency": 105,
        "org": "Comcast Cable Communications, LLC",
        "port": "8080",
        "protocols": "http",
        "region": None,
        "responseTime": 914,
        "speed": 344,
        "updated_at": "2023-04-20T13:01:12.376Z",
        "workingPercent": None,
        "upTime": 100,
        "upTimeSuccessCount": 1368,
        "upTimeTryCount": 1368,
    },
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
]
HEADER = {
    "User-Agent": None,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}


def random_header():
    agent = random.choice(USER_AGENTS)
    header = deepcopy(HEADER)
    header["User-Agent"] = agent
    return header


def random_proxy():
    proxy = random.choice(PROXIES)
    return {proxy["protocols"]: proxy["ip"]}
