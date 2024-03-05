import pkgutil
from crawlers.base import BaseCrawler
# 初始化一个空列表来存储子类
CRAWLER_CLASS_LIST = []

# 遍历当前包及其子包中的所有模块
for importer, modname, ispkg in pkgutil.walk_packages(__path__):
    # 动态导入模块
    module = importer.find_module(modname).load_module(modname)

    # 检查模块中的每个类，看它是否是BaseClass的子类
    for _, cls in vars(module).items():
        if isinstance(cls, type) and issubclass(cls, BaseCrawler) and cls is not BaseCrawler:
            CRAWLER_CLASS_LIST.append(cls)
            # 现在，subclasses列表包含了所有继承自BaseClass的子类