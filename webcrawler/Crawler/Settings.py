import yaml
import os
import annotation

path = os.path.abspath(os.path.dirname(__file__))

# 获取yaml文件路径
yamlPath = os.path.join(path, 'config.yaml')

@annotation.Singleton
class Settings:
    def __init__(self):
        super().__init__()
        with open(yamlPath, 'rb') as f:
            data = yaml.safe_load_all(f)
            self.config = next(data)
    
    def getConfig(self, key):
        return self.config.get(key, None)

if __name__ == '__main__':
    s = Settings()
    print(s.getConfig('database'))