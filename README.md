# rime-pyjj-wubi

rime-pyjj-wubi 是一个用于生成 Rime 输入法“拼音加加双拼+整句五笔辅码筛选” (PyJJ Wubi) 相关数据和词库的项目。它整合了来自多个上游项目的拼音、词频、五笔码表及
Emoji 数据，并进行转换、合并与优化，旨在为 Rime 提供更加丰富且准确的输入体验。

## 使用说明

本项目是给 [rime-config](https://github.com/oyyq99999/rime-config.git)
这个项目提供数据更新用的，单独使用很麻烦。拼音词典部分和[caspal_wubi86.dict.yaml](generated/caspal_wubi86.dict.yaml)
可以试着单独拿出来使用。

## 主要功能

* **五笔 86 词库生成**：基于 `rime-wubi` 和 `rime-wubi86-ext` 生成基础及扩展词库。
* **拼音词频整合**：融合 `jieba` 大词库、`pinyin-data` 和 `phrase-pinyin-data` 的拼音及词频信息。
* **Emoji 支持**：通过 `simplified_emoji.py` 处理 `rime-emoji` 数据，支持简体中文环境下的 Emoji 联想。
* **大字符集覆盖**：支持生成涵盖 Unicode 字符集（目前是 Unicode 17）的拼音及五笔词库。
* **自动化构建**：使用 `Makefile` 管理生成流程，简化更新步骤。

## 环境要求

* **Python**: >= 3.12
* **依赖管理工具**: [uv](https://github.com/astral-sh/uv)
* **构建工具**: `make`
* **系统库**: `libicu` (用于 `pyicu`)

## 快速开始

### 1. 克隆项目

克隆时请包含子模块（**但一定不要recursive**，因为`pinyin-data`和`phrase-pinyin-data`这两个项目存在互相引用）：

```bash
git clone https://github.com/oyyq99999/rime-pyjj-wubi.git
cd rime-pyjj-wubi
git submodule update --init
```

### 2. 安装依赖

项目使用 `uv` 管理虚拟环境和依赖：

```bash
uv sync
```

### 3. 生成词库数据

直接运行 `make` 命令即可开始生成所有 `.dict.yaml` 和 Emoji 文本文件：

```bash
make
```

生成的词库文件将位于 `generated/` 目录下，Emoji 数据位于 `opencc/` 目录下。

## 项目结构

* `generate_dict.py`: 主脚本，用于生成最终的 Rime 词库文件。
* `combine_wubi.py`: 负责合并多个五笔码表源文件。
* `simplified_emoji.py`: 将繁体 Emoji 映射转换为简体，并添加国旗支持。
* `parse_pinyin_and_freq.py`: 解析拼音和词频数据。
* `parse_phrase_pinyin_data.py`: 处理长词拼音数据。
* `libs/`: 存放所有上游依赖项目的子模块。
* `data/`: 存放手动维护的补丁或扩展数据（如 `extend_phrase_pinyin.txt`）。
* `Makefile`: 定义了自动构建的任务逻辑。

## 上游致谢

本项目的数据源高度依赖于以下优秀的开源项目：

* [rime-wubi](https://github.com/rime/rime-wubi) & [rime-wubi86-ext](https://github.com/yanhuacuo/rime-wubi86-ext):
  五笔基础与扩展码表。
* [pinyin-data](https://github.com/mozillazg/pinyin-data) & [phrase-pinyin-data](https://github.com/mozillazg/phrase-pinyin-data):
  汉字与长词拼音数据。
* [jieba](https://github.com/fxsjy/jieba): 词频参考数据。
* [rime-emoji](https://github.com/rime/rime-emoji): Emoji 联想转换。
* [OpenCC](https://github.com/BYVoid/OpenCC): 繁简转换支持。

## 许可证

本项目遵循 [GPL-3.0-only](LICENSE) 开源许可协议。生成的词库数据由于基于 `rime-wubi86-ext` (GPL v3)，也同样适用该协议。
