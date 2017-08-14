# pylint: disable=no-self-use,invalid-name
import json
from unittest import TestCase

from allennlp.common import Params
from allennlp.common.params import replace_none
from allennlp.service.servable.models.semantic_role_labeler import SemanticRoleLabelerServable


class TestSrlServable(TestCase):
    def test_uses_named_inputs(self):
        inputs = {
                "sentence": "The squirrel wrote a unit test to make sure its nuts worked as designed."
        }

        with open('experiment_config/semantic_role_labeler.json') as f:
            config = json.loads(f.read())
            config['trainer']['serialization_prefix'] = 'tests/fixtures/srl'
            config['model']['text_field_embedder']['tokens']['pretrained_file'] = \
                'tests/fixtures/glove.6B.100d.sample.txt.gz'
            srl_config = Params(replace_none(config))

        model = SemanticRoleLabelerServable.from_config(srl_config)

        result = model.predict_json(inputs)

        # TODO(joelgrus): update this when you figure out the result format
        verbs = result.get("verbs")

        assert verbs is not None

        assert any(v["verb"] == "wrote" for v in verbs)
        assert any(v["verb"] == "make" for v in verbs)
        assert any(v["verb"] == "worked" for v in verbs)
