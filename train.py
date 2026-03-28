
import os
from dotenv import load_dotenv
load_dotenv()

import dspy
from dspy import LM
from dspy.teleprompt import BootstrapFewShot
lm = LM("openai/gpt-4o")
dspy.settings.configure(lm=lm)

class DecompileSignature(dspy.Signature):
    assembly = dspy.InputField()
    code = dspy.OutputField()

class Decompiler(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(DecompileSignature)

    def forward(self, assembly):
        return self.predict(assembly=assembly)

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

# optimization
optimizer = BootstrapFewShot(metric=None)
compiled = optimizer.compile(Decompiler(), trainset=trainset)

# test
result = compiled(assembly="int FUN(int z){int w=z*3;return w;}")

print(result.code)

compiled.save("compiled_dspy.json")

