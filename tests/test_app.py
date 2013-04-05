import os
import webtest

class TestApplication(object):
    
    def test_app(self):
        here = os.path.dirname(__file__)
        app_root = os.path.join(here, 'testapp')
        from makky import main
        app = webtest.TestApp(main({}, root=app_root))

        res = app.get('/?message=Hello+Makky')
        
        assert "Hello Makky" in res

        res = app.get('/sub?x=1')

        assert res.location == 'http://localhost/sub/?x=1'

        res = app.get(res.location)
        assert u"this is sub\n" == res.text
