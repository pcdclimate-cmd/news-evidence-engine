import unittest
from engine import analyze

def e(group='a', direction='support', strength=5, source_type='primary'):
    return dict(description='Testbelägg', group=group, direction=direction, strength=strength, source_type=source_type)

class EngineTests(unittest.TestCase):
    def test_no_evidence_is_unknown(self):
        r = analyze({'claim':'Ett testpåstående', 'evidence':[]})
        self.assertIsNone(r['evidence_index'])
        self.assertEqual(r['verdict'], 'Otillräckligt underlag')
    def test_repeated_same_origin_not_double_counted(self):
        r1=analyze({'claim':'Ett testpåstående','evidence':[e()]})
        r2=analyze({'claim':'Ett testpåstående','evidence':[e(),e()]})
        self.assertEqual(r1['evidence_index'],r2['evidence_index'])
        self.assertEqual(r2['counted_count'],1)
    def test_support_and_refute_cancel(self):
        r=analyze({'claim':'Ett testpåstående','evidence':[e('a'),e('b','refute')]})
        self.assertEqual(r['evidence_index'],50)
        self.assertEqual(r['verdict'],'Motstridiga belägg')
    def test_independent_evidence_increases_support(self):
        r1=analyze({'claim':'Ett testpåstående','evidence':[e('a')]})
        r2=analyze({'claim':'Ett testpåstående','evidence':[e('a'),e('b')]})
        self.assertGreater(r2['evidence_index'],r1['evidence_index'])
    def test_invalid_data_rejected(self):
        with self.assertRaises(ValueError): analyze({'claim':'Ett testpåstående','evidence':[dict(e(),strength=7)]})

if __name__ == '__main__': unittest.main()
