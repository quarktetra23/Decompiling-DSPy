import os
os.environ["OPENAI_API_KEY"] = "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"

import dspy
from dspy import LM
from dspy.teleprompt import BootstrapFewShot

# setup
lm = LM("openai/gpt-4o")
dspy.settings.configure(lm=lm)

# signature
class DecompileSignature(dspy.Signature):
    assembly = dspy.InputField()
    code = dspy.OutputField()

# module
class Decompiler(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(DecompileSignature)

    def forward(self, assembly):
        return self.predict(assembly=assembly)

# 🔥 TRAINING DATA (start small)
trainset = [
    dspy.Example(
        assembly="int FUN(int a){int b=a*2;return b;}",
        code="int func(int a) { return a * 2; }"
    ).with_inputs("assembly"),

    dspy.Example(
        assembly="int FUN(int x){int y=x+1;return y;}",
        code="int func(int x) { return x + 1; }"
    ).with_inputs("assembly"),
]

# optimizer
optimizer = BootstrapFewShot(metric=None)

compiled = optimizer.compile(Decompiler(), trainset=trainset)

# test
result = compiled(assembly="int FUN(int z){int w=z*3;return w;}")

print(result.code)

compiled.save("compiled_dspy.json")

