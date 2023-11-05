
class DefaultCookiePool:
    def getCookie(self):
        raise NotImplementedError

class ZillowCookiePool(DefaultCookiePool):
    def getCookie(self):
        return 'x-amz-continuous-deployment-state=AYABeM%2Fqb0VUBV1S1RsZkUnkJjkAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADMtr8y4kPG2DCfv5pgAw%2FT8BNtzmrskaCQ2T3Y%2FUyIOQEoF9tOVJdjJMc5nqaIoygnDYzxUew4cr1NVE9PfBAgAAAAAMAAQAAAAAAAAAAAAAAAAAAF%2FzjepuM4TyW4U4kj4Qinz%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAxRvpVjnQZx87Y%2FogXxfgyl8IjhKtdH%2Ftj1gfqX; zguid=24|%24cbc80d3e-40e3-4196-9c57-3cc27b40e98f; _ga=GA1.2.1836450175.1696808577; zjs_anonymous_id=%22cbc80d3e-40e3-4196-9c57-3cc27b40e98f%22; zg_anonymous_id=%22c5b7b2c5-0b8e-497b-94ff-94db0f50547a%22; _pxvid=6a68bd92-6634-11ee-891f-a6f2cb4baf1b; _gcl_au=1.1.447866034.1696808717; __pdst=4a8ea1cb5df140eda2c6ebadbcf9daa1; _fbp=fb.1.1696808719038.876560113; _pin_unauth=dWlkPU5UQm1Oakk0TXpJdE1EWTRaUzAwWW1ReExUaGxZV1l0TlRSbVpERTRZMkV4TnpCaw; g_state={"i_l":0}; loginmemento=1|7eaf08388401adf9f184b1cecdcf6cbf36a2681b53dc0b26ab6c9b7ff13ede00; userid=X|3|52219b738ca8c8dc%7C6%7CUgNFTvUqFY_9x1QVzwab279Qxrz2Gm2yoDVAA5l4OWo%3D; zjs_user_id=%22X1-ZUrlkk6sgvxqtl_9vdv6%22; _derived_epik=dj0yJnU9dTlHTEdqY3o4eGhSYW1vdlVUaDNSVy1RUVk4YUpYaWUmbj1jV0JQenVmaFZ6U2JHazJjTEtDQW1BJm09NCZ0PUFBQUFBR1VqUkpVJnJtPTQmcnQ9QUFBQUFHVWpSSlUmc3A9NA; _hp2_id.1215457233=%7B%22userId%22%3A%227479187844433750%22%2C%22pageviewId%22%3A%223174317463964373%22%2C%22sessionId%22%3A%22503128611613509%22%2C%22identity%22%3A%22X1-ZUrlkk6sgvxqtl_9vdv6%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; zgsession=1|3917eb0a-d723-48d7-9a17-6a1336f8b97d; _gid=GA1.2.1749589228.1698557503; pxcts=71c37197-761c-11ee-a996-8f0b021a09cd; DoubleClickSession=true; _clck=15s43cq|2|fga|0|1376; JSESSIONID=7B56002EE3FC60A48D129AAFE85AC0D1; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEsBJe8r2eG%2BRDmFA13Groupx9dS4BCAODABHq68P4cLWCvtl0adm6aRLUuirnd5YtPWBxM6jwuGrp8wS6A; __gads=ID=a584bba4effab93f:T=1696808717:RT=1698655168:S=ALNI_MaskXlGv8wkuPhbSTJLIZDo9OFJpA; __gpi=UID=00000a0b013ffd54:T=1696808717:RT=1698655168:S=ALNI_MYER-NTMUzy7Wexw93d6yYIDGC7Ig; tfpsi=b24bb7dc-9c38-4a18-b0c5-aef78fe18fef; _gat=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1; AWSALB=tQ5i7ETdb9cGbjigq1kDuN09PCwkBf64+e+bjeryuy6hNHYx1Che47MLAXbfnzH8w0tw3SYMEtfVBUK1heg4ZJECU+T4UR+VAWV6nbKxyBSgf8nqlmLduTSrgkEH; AWSALBCORS=tQ5i7ETdb9cGbjigq1kDuN09PCwkBf64+e+bjeryuy6hNHYx1Che47MLAXbfnzH8w0tw3SYMEtfVBUK1heg4ZJECU+T4UR+VAWV6nbKxyBSgf8nqlmLduTSrgkEH; search=6|1701247361673%7Crect%3D47.619277034294356%252C-122.33899849858093%252C47.609223846800816%252C-122.36459750141907%26rid%3D99580%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0999580%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _px3=972959c1fa07e487583b4ce528afbb553a75a0d39a7b219dc7f4ed1a35b30f16:qopc2AoLm0myzqzoHdl1J3GSA1zPOBhLz79SbTBXIBZR2lZA7p/lcTuI7dgBJug8voExMERfmP2mvnVY7W/Xig==:1000:kYlIOdMAD6/6UX1Eda1Qu4VTaduvkdjvB+4ccx+8d9qQyI57q5IZEfe85miNdUoMNy6nw/7zGlf9lxVJTBFEJgjyLR46tnM4FiDRk0R2WGSWwtBkKEGH6Q3MOQ5ujrfKdiCdML5z1Y65twclE/000rB5z9U0gxgN4XKPom/78MQaV+ldoEwZS7d2btCQIHGh4siu35EnSfsufbMoH7YQJSyZ0aACWSOqWyZ5BKpIWSg=; _uetsid=736f6140761c11ee8a10d38da1db9c7f; _uetvid=bc156a70663411ee8e35259eb8e1912e; _clsk=wassif|1698655367537|3|0|u.clarity.ms/collect'


CookiePoolDict = {
    'zillow': ZillowCookiePool()
}

def getCookie(key):
    CookiePool = CookiePoolDict.get(key, DefaultCookiePool())
    return CookiePool.getCookie()