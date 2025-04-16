import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 就是为了让 Python 能够找到 app 目录，那么如app.models.message就能导入
# 不会报错ModuleNotFoundError: No module named 'app'


import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 