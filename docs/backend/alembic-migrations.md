# 使用 Alembic 进行数据库迁移

Alembic 是 SQLAlchemy 的轻量级数据库迁移工具。它允许您以结构化和版本控制的方式管理数据库模式随时间的变化。

## 为什么使用 Alembic？

*   **数据库的版本控制：** 与应用程序代码一起跟踪模式更改。
*   **可重复部署：** 确保不同环境（开发、 staging、生产）之间一致的数据库模式。
*   **协作：** 使多个开发人员更容易在数据库模式更改上工作而不会发生冲突。
*   **自动化模式更改：** 避免手动 SQL 脚本进行模式修改，减少错误。

## 核心概念

*   **迁移环境：** 包含 Alembic 配置和迁移脚本的目录（通常在您的后端根目录中名为 `alembic` 或 `alembic`）。
*   **`alembic.ini`：** Alembic 的主配置文件。它指定数据库连接详细信息、脚本位置和其他设置。
*   **`env.py`：** 迁移环境中的 Python 脚本，Alembic 在运行命令时执行。这是您配置 Alembic 如何连接到数据库以及如何发现 SQLAlchemy 模型以进行自动生成的地方。
    *   关键的是，`env.py` 需要了解您的 SQLAlchemy 模型的元数据（`target_metadata = Base.metadata`）。
*   **修订：** 表示对数据库模式的一组更改的单个迁移脚本。每个修订都有一个唯一的 ID。
*   **`upgrade()` 函数：** 包含应用模式更改的操作（例如，创建表、添加列）。
*   **`downgrade()` 函数：** 包含回滚模式更改的操作。

## 设置 Alembic（如果尚未设置）

如果 Alembic 还不是项目的一部分，您通常会初始化它：

1.  安装 Alembic：`pip install alembic`
2.  初始化环境（从您的 `backend` 目录）：
    ```bash
    alembic init alembic
    ```
    （这将创建一个 `alembic` 目录和一个 `alembic.ini` 文件。）
3.  使用数据库 URL 配置 `alembic.ini`（`sqlalchemy.url`）。
4.  配置 `alembic/env.py`：
    *   确保 `target_metadata` 指向来自 `app.db.base` 或定义模型的位置的 SQLAlchemy `Base.metadata`。
    *   确保 Python 路径已设置，以便 `env.py` 可以导入您的应用程序模块。

## 常用 Alembic 命令

从包含 `alembic.ini` 的目录（通常是您的 `backend` 根目录）运行这些命令。

### 1. 生成新的迁移脚本

当您对 SQLAlchemy 模型进行更改（例如，添加新模型、向现有模型添加列）时，您需要生成迁移脚本。

**手动修订（推荐用于理解）：**
```bash
alembic revision -m "create_users_table"
```
这将在 `alembic/versions/` 中创建一个新的空迁移文件。然后您手动编辑此文件以使用 Alembic 的 `op` 对象定义 `upgrade()` 和 `downgrade()` 函数。

**示例（手动 - 创建用户表）：**
```python
# 在生成的 migration_xyz.py 文件中
from alembic import op
import sqlalchemy as sa

# 修订标识符，由 Alembic 使用。
revision = 'your_revision_id'
down_revision = 'previous_revision_id_or_None'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True)
    )

def downgrade():
    op.drop_table('users')
```

**自动生成修订（谨慎使用并始终审查）：**
Alembic 可以比较您的 SQLAlchemy 模型与当前数据库状态，并尝试自动生成迁移脚本。

```bash
alembic revision -m "add_bio_to_users" --autogenerate
```
*   **重要：** 始终仔细审查自动生成的脚本。Alembic 可能无法完美检测所有更改（例如，复杂约束、服务器默认值、对不直接的类型更改）。您可能需要手动调整脚本。

### 2. 应用迁移

要将待处理的迁移应用到数据库：

*   **应用所有待处理的迁移（升级到最新修订）：**
    ```bash
    alembic upgrade head
    ```
*   **应用迁移到特定修订：**
    ```bash
    alembic upgrade <revision_id>
    ```
*   **应用单个下一个迁移：**
    ```bash
    alembic upgrade +1
    ```

### 3. 回滚迁移（降级）

要撤销迁移：

*   **回滚最后应用的迁移：**
    ```bash
    alembic downgrade -1
    ```
*   **回滚到特定修订：**
    ```bash
    alembic downgrade <target_revision_id>
    ```
*   **回滚所有迁移（到空数据库状态，如果适用）：**
    ```bash
    alembic downgrade base
    ```
    **（在生产数据上使用时要极其谨慎！）**

### 4. 查看迁移状态

*   **显示当前修订和迁移历史：**
    ```bash
    alembic history
    ```
*   **显示数据库当前所在的修订 ID：**
    ```bash
    alembic current
    ```
*   **显示所有修订，指示哪些已应用：**
    ```bash
    alembic history --verbose
    ```

## 最佳实践

*   **保持迁移小而专注：** 每个迁移应该代表一个单一的、逻辑的更改。
*   **测试迁移：** 在将迁移应用到生产之前，始终在开发或 staging 环境中测试您的迁移。
*   **永远不要编辑已应用的迁移：** 一旦迁移已应用到共享数据库（如生产），不要编辑其脚本。相反，创建新迁移来纠正或更改它。
*   **备份数据库：** 在生产上运行重要迁移之前，始终备份数据库。
*   **审查自动生成的脚本：** 彻底检查使用 `--autogenerate` 生成的任何脚本。
*   **单独考虑数据迁移：** 对于涉及转换数据的更改（不仅仅是模式），您可能在迁移脚本中编写自定义 Python 代码或将其作为单独过程处理。Alembic 的 `op.bulk_insert` 和 `op.execute` 在这里很有用。

## 进一步阅读

*   [Alembic 官方教程](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
*   [Alembic 操作参考](https://alembic.sqlalchemy.org/en/latest/ops.html)
