
class DefaultCookiePool:
    def getCookie(self):
        raise NotImplementedError

class ZillowCookiePool(DefaultCookiePool):
    def getCookie(self):
        return r'_ga=GA1.2.1836450175.1696808577; zg_anonymous_id=%22c5b7b2c5-0b8e-497b-94ff-94db0f50547a%22; _pxvid=6a68bd92-6634-11ee-891f-a6f2cb4baf1b; _gcl_au=1.1.447866034.1696808717; __pdst=4a8ea1cb5df140eda2c6ebadbcf9daa1; _fbp=fb.1.1696808719038.876560113; _pin_unauth=dWlkPU5UQm1Oakk0TXpJdE1EWTRaUzAwWW1ReExUaGxZV1l0TlRSbVpERTRZMkV4TnpCaw; g_state={"i_l":0}; pxcts=8b6762ae-7b6e-11ee-afcc-f60768005684; DoubleClickSession=true; _derived_epik=dj0yJnU9QVlJUXhObktUUW5lQkoxdGhJM1Q0WUJYbE5vZXRGNFQmbj1NVlY4dl9zRnJrcVhwV181SzJCYkN3Jm09NCZ0PUFBQUFBR1ZISmUwJnJtPTQmcnQ9QUFBQUFHVkhKZTAmc3A9Mg; _gid=GA1.2.1210237375.1699251865; tfpsi=e02b1414-6ab4-430f-990f-e1342c76efe8; _clck=15s43cq|2|fgh|0|1376; zgsession=1|75a61b33-de04-409d-a39d-d7e8c01592f2; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1; zguid=24|%2494d0bf96-5b09-479f-a144-68b069b48a0f; zjs_anonymous_id=%2294d0bf96-5b09-479f-a144-68b069b48a0f%22; JSESSIONID=FBC3E06717734677560FB74AB0E2DE63; userid=X|3|5a706d1e41f2cc28%7C8%7CfN4qKyGFdCcugC8-YLvC1-rvkVGyx6ANNgTCwKS799o%3D; loginmemento=1|020e8a48db6e58ce09fa5ca136cc70cb173450a11c321bee38ebc2443893be12; ZILLOW_SSID=1|AAAAAVVbFRIBVVsVEmztOWarof%2FtRay1CuX5O3ZsW5hMId1JXYKhuN8UcxPy8pK90fmjA5RB%2FdCAe30I0IrkdFw6ZRmugVUPPA; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEiA4OwmNpFJ0QGNsbQu0XCyhbAjeJNalj1aUG%2FbNfN6bTjDkzhq7pTZsR3fUG3FkFkRdxsqN%2BQ1FkCyCww; _gat=1; zjs_user_id=%22X1-ZU16vsvb6b016vd_8nu8j%22; _hp2_id.1215457233=%7B%22userId%22%3A%224468324536685916%22%2C%22pageviewId%22%3A%223208962130782672%22%2C%22sessionId%22%3A%227327898598487803%22%2C%22identity%22%3A%22X1-ZU16vsvb6b016vd_8nu8j%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D; _hp2_ses_props.1215457233=%7B%22r%22%3A%22https%3A%2F%2Fwww.zillow.com%2F%3Fautosignin%3Dfalse%22%2C%22ts%22%3A1699252130042%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%2C%22q%22%3A%22%3Fautosignin%3Dfalse%22%7D; AWSALB=cfXF97hzFbqmW7u2heUzx1jkTTzY8um8J7BB4+uEixjK/LButFbZoqyVYDEsjHpVDogXMx7uU6Eh0UzGVC+VU/h9ku9txr6Vw/hDpc7MLpsM1fWSnuxirtXTQpfr; AWSALBCORS=cfXF97hzFbqmW7u2heUzx1jkTTzY8um8J7BB4+uEixjK/LButFbZoqyVYDEsjHpVDogXMx7uU6Eh0UzGVC+VU/h9ku9txr6Vw/hDpc7MLpsM1fWSnuxirtXTQpfr; search=6|1701844174326%7Crect%3D47.63435319174181%2C-122.31695074047852%2C47.59414044161253%2C-122.38664525952149%26rid%3D99580%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0999580%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _px3=139a5f3a9f02f1730efbc5ba8d5118ca20b1a29cbc0c0560277ad07d0f181076:4aJV3mYMYJpLkSkXlT5tbDGtdhFR9+NPv/9/vzHPI1Q1k1hHno1/8bcWmKgipmGJQMrXpHtCUvvNKi3/gVTE2w==:1000:3jkiGiJEOO9Kumxlx9AsCUqT+FqosrRSu0+N3T6sz7DFgp8HloJR4f7vN4ne0BED6eSROZ7f3VGLt4AsLUeCsTa9mhiTXwQi2nwTVFUU2+FMJq/bGHQD+rOj10fQthkPwgFMYC4B8QKcN3u/ajEGvxNdmTs1EvYIiTWGRZqtk4I01RRUfaPdpIEEyt0VO7FxJ++Y0XJ+xakN6vElKL23vaxr/H4E02mWgcviGLS7v7w=; __gads=ID=a584bba4effab93f:T=1696808717:RT=1699252176:S=ALNI_MaskXlGv8wkuPhbSTJLIZDo9OFJpA; __gpi=UID=00000a0b013ffd54:T=1696808717:RT=1699252176:S=ALNI_MYER-NTMUzy7Wexw93d6yYIDGC7Ig; _uetsid=23a370207c6d11eeb98e474a28b36a51; _uetvid=bc156a70663411ee8e35259eb8e1912e; _clsk=woy9tz|1699252178868|13|0|x.clarity.ms/collect'


class RealtorCookiePool(DefaultCookiePool):
    def getCookie(self):
        return ""

CookiePoolDict = {
    'zillow': ZillowCookiePool(),
    'realtor': RealtorCookiePool()
}

def getCookie(key):
    CookiePool = CookiePoolDict.get(key, DefaultCookiePool())
    return CookiePool.getCookie()