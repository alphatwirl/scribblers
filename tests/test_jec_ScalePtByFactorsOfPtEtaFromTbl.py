import unittest
import cStringIO

from ..jec import ScalePtByFactorOfPtEtaFromTbl

##__________________________________________________________________||
tbl_corr_txt = """
 jet_eta   jet_pt    corr
    -1.5  26.8573  1.1774
    -0.5  26.9680  1.1726
     0.5  26.8664  1.1770
    -1.5  29.9007  1.1866
    -0.5  29.9091  1.1863
     0.5  29.9087  1.1863
    -1.5  33.6483  1.1831
    -0.5  33.5149  1.1878
     0.5  33.6616  1.1826
    -1.5  38.0716  1.1732
    -0.5  37.8125  1.1813
     0.5  38.0745  1.1731
    -1.5  43.1789  1.1607
    -0.5  42.8457  1.1697
     0.5  43.1845  1.1605
    -1.5  48.9785  1.1481
    -0.5  48.6125  1.1567
     0.5  48.9852  1.1479
    -1.5  55.4928  1.1370
    -0.5  55.0816  1.1454
     0.5  55.4958  1.1369
    -1.5  62.7913  1.1274
    -0.5  62.3670  1.1351
     0.5  62.8012  1.1272
    -1.5  71.0061  1.1186
    -0.5  70.5147  1.1264
     0.5  71.0092  1.1186
    -0.5  79.6702  1.1186
    -0.5  89.9425  1.1118
"""[1:] # to remove the fist line break

##__________________________________________________________________||
class Test_ObjectCorrection(unittest.TestCase):

    def setUp(self):
        f = cStringIO.StringIO(tbl_corr_txt)
        self.obj = ScalePtByFactorOfPtEtaFromTbl(
            tbl_corr_path = f,
            valid_eta_range = (-3, 3),
            default_scale_factor = 0.8,
        )

    def tearDown(self):
        pass

    def test_repr(self):
        repr(self.obj)

    def test_call(self):
        self.assertAlmostEqual(44.83949, self.obj(pt = 37.9, eta = -0.8))

    def test_scale_factor_simple(self):
        self.assertEqual(1.1831, self.obj.scale_factor(pt = 37.9, eta = -0.8))
        self.assertEqual(1.1813, self.obj.scale_factor(pt = 37.9, eta = -0.4))
        self.assertEqual(1.1732, self.obj.scale_factor(pt = 38.1, eta = -0.8))

        # the last pt bin for each eta bin
        self.assertEqual(1.1186, self.obj.scale_factor(pt = 500.0, eta = -1.2))
        self.assertEqual(1.1118, self.obj.scale_factor(pt = 500.0, eta = 0.2))
        self.assertEqual(1.1186, self.obj.scale_factor(pt = 500.0, eta = 0.8))

    def test_scale_factor_out_of_range_pt(self):
        self.assertEqual(1.1726, self.obj.scale_factor(pt = 20.1, eta = 0.2))

    def test_scale_factor_out_of_range_eta_from_tbl(self):
        self.assertEqual(0.8, self.obj.scale_factor(pt = 50.2, eta = -2.2))

    def test_scale_factor_out_of_range_eta_by_option(self):
        self.assertEqual(0.8, self.obj.scale_factor(pt = 50.2, eta = -3.1))
        self.assertEqual(0.8, self.obj.scale_factor(pt = 50.2, eta = 3.1))

##__________________________________________________________________||
