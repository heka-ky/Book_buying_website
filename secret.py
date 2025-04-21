# 生成安全密钥的代码示例
import secrets

# 生成一个安全的随机密钥(64个字符的十六进制字符串)
secret_key = secrets.token_hex(32)

# 输出示例(不要直接使用这个值，每次运行都会生成不同的值)
print("生成的FLASK_SECRET_KEY:", secret_key)