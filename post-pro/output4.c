#include "out.h"



int _f(int param_1)

{
  int iVar1;
  undefined4 local_18;
  
  local_18 = param_1;
  if (1 < param_1) {
    local_18 = _f(param_1 + -1);
    iVar1 = _f(param_1 + -2);
    local_18 = local_18 + iVar1;
  }
  return local_18;
}



void entry(void)

{
  _f(5);
  return;
}



