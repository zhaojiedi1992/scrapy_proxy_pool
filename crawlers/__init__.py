# import pkgutil
# from crawlers.base import BaseCrawler
# # 初始化一个空列表来存储子类
# CRAWLER_CLASS_LIST = []
#
# # 遍历当前包及其子包中的所有模块
# for importer, modname, ispkg in pkgutil.walk_packages(__path__):
#     # 动态导入模块
#     module = importer.find_module(modname).load_module(modname)
#
#     # 检查模块中的每个类，看它是否是BaseClass的子类
#     for _, cls in vars(module).items():
#         if isinstance(cls, type) and issubclass(cls, BaseCrawler) and cls is not BaseCrawler:
#             CRAWLER_CLASS_LIST.append(cls)
#             # 现在，subclasses列表包含了所有继承自BaseClass的子类

import pkgutil
import importlib.util

from crawlers.base import BaseCrawler

# 初始化一个空列表来存储子类
CRAWLER_CLASS_LIST = []

# 遍历当前包及其子包中的所有模块
for importer, modname, ispkg in pkgutil.walk_packages(__path__, prefix='crawlers.'):
    # 使用importlib.util.find_spec和importlib.util.module_from_spec来动态导入模块
    # 这比直接使用importer.find_module().load_module()更现代且更安全
    spec = importlib.util.find_spec(modname)
    if spec is None:
        continue  # 如果找不到模块规格，则跳过
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # 执行模块，填充其命名空间

    # 检查模块中的每个类，看它是否是BaseCrawler的子类且不是BaseCrawler本身
    for attr_name, cls in vars(module).items():
        if isinstance(cls, type) and issubclass(cls, BaseCrawler) and cls is not BaseCrawler:
            CRAWLER_CLASS_LIST.append(cls)

# 现在，CRAWLER_CLASS_LIST包含了所有继承自BaseCrawler的子类