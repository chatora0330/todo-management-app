from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)

from database import get_db
from forms import TodoForm

bp = Blueprint(
    "todo",
    __name__,
)

PER_PAGE = 10

@bp.route("/")
@login_required
def index():

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    )

    priority = request.args.get(
        "priority",
        ""
    )
    
    sort = request.args.get(
        "sort",
        "created_desc"
    )
    
    page = request.args.get(
        "page",
        1,
        type=int
    )
    
    if page < 1:
        page = 1
        
    offset = (page - 1) * PER_PAGE
    
    db = get_db()
    
    # where句

    where = """
        WHERE user_id = ?
    """

    params = [
        current_user.id
    ]
    
    # タイトル検索
    if keyword:

        where += """
            AND title LIKE ?
        """

        params.append(
            f"%{keyword}%"
        )

    # ステータス絞り込み
    if status:

        where += """
            AND status = ?
        """

        params.append(status)

    # 優先度絞り込み
    if priority:

        where += """
            AND priority = ?
        """

        params.append(priority)
        
    # 並び替え
    sort_options = {
        
        "created_desc":
            "created_at DESC",
            
        "created_asc":
            "created_at ASC",
            
        "deadline_asc":
            "deadline ASC",
            
        "deadline_desc":
            "deadline DESC",
        
        "priority":
            """
            CASE priority
                WHEN '高' THEN 1
                WHEN '中' THEN 2
                WHEN '低' THEN 3
                ELSE 4
            END ASC
            """,
    }
    
    order_by = sort_options.get(
        sort,
        "created_at DESC"
    )
    
    # 総件数
    
    count_query = f"""
        SELECT COUNT(*)
        FROM todos
        {where}    
    """
    
    total = db.execute(
        count_query,
        params
    ).fetchone()[0]
    
    
    query = f"""
        SELECT *
        FROM todos
        {where}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
    """
    
    todo_params = params + [
        PER_PAGE,
        offset,
    ]

    todos = db.execute(
        query,
        todo_params
    ).fetchall()
    
    # 総ページ数
    
    total_pages = (
        total + PER_PAGE -1
    ) // PER_PAGE

    return render_template(
        "todo_list.html",
        todos=todos,
        keyword=keyword,
        status=status,
        priority=priority,
        sort=sort,
        page=page,
        total_pages=total_pages,
    )

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        priority = request.form["priority"]
        status = request.form["status"]
        deadline = request.form["deadline"]

        if not title:
            flash("タイトルを入力してください。", "danger")
            return redirect(url_for("todo.add"))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db = get_db()

        db.execute(
            """
            INSERT INTO todos(
                user_id,
                title,
                description,
                status,
                priority,
                deadline,
                created_at,
                updated_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                current_user.id,
                title,
                description,
                status,
                priority,
                deadline,
                now,
                now,
            ),
        )

        db.commit()

        flash("ToDoを追加しました。", "success")

        return redirect(url_for("todo.index"))

    return render_template("todo_add.html")


@bp.route("/<int:todo_id>/edit", methods=["GET", "POST"])
@login_required
def edit(todo_id):

    db = get_db()

    todo = db.execute(
        """
        SELECT *
        FROM todos
        WHERE id = ?
          AND user_id = ?
        """,
        (todo_id, current_user.id),
    ).fetchone()

    if todo is None:
        flash("指定されたToDoが見つかりません。", "danger")
        return redirect(url_for("todo.index"))

    form = TodoForm()

    if form.validate_on_submit():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.execute(
            """
            UPDATE todos
            SET
                title = ?,
                description = ?,
                status = ?,
                priority = ?,
                deadline = ?,
                updated_at = ?
            WHERE id = ?
              AND user_id = ?
            """,
            (
                form.title.data,
                form.description.data,
                form.status.data,
                form.priority.data,
                (
                    form.deadline.data.strftime("%Y-%m-%d")
                    if form.deadline.data
                    else None
                ),
                now,
                todo_id,
                current_user.id,
            ),
        )

        db.commit()

        flash("ToDoを更新しました。", "success")

        return redirect(url_for("todo.index"))

    if request.method == "GET":
        form.title.data = todo["title"]
        form.description.data = todo["description"]
        form.priority.data = todo["priority"]
        form.status.data = todo["status"]

        if todo["deadline"]:
            form.deadline.data = datetime.strptime(todo["deadline"], "%Y-%m-%d").date()

    return render_template(
        "todo_edit.html",
        form=form,
        todo=todo,
    )

@bp.route("/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete(todo_id):

    db = get_db()
    
    todo = db.execute(
        """
        SELECT id
        FROM todos
        WHERE id = ?
          AND user_id = ?
        """,
        (
            todo_id,
            current_user.id,
        ),
    ).fetchone()
    
    if todo is None:
        flash("指定されたToDoが見つかりません。", "danger")
        return redirect(url_for("todo.index"))
    
    db.execute(
        """
        DELETE FROM todos
        WHERE id = ?
          AND user_id = ?
        """,
        (
            todo_id,
            current_user.id,
        ),
    )
    
    db.commit()
    
    flash("ToDoを削除しました。", "success")
    
    return redirect(url_for("todo.index"))

@bp.route("/<int:todo_id>/status", methods=["POST"])
@login_required
def update_status(todo_id):
    
    status = request.form.get("status")
    
    allowed_statuses = [
        "未着手",
        "進行中",
        "完了",
    ]
    
    if status not in allowed_statuses:
        flash("不正なステータスです。", "danger")
        return redirect(url_for("todo.index"))
    
    db = get_db()
    
    todo = db.execute(
        """
        SELECT id
        FROM todos
        WHERE id = ?
          AND user_id = ?
        """,
        (
            todo_id,
            current_user.id,
        ),
    ).fetchone()
    
    if todo is None:
        flash("指定されたToDoが見つかりません。", "danger")
        return redirect(url_for("todo.index"))
    
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    
    db.execute(
        """
        UPDATE todos
        SET
            status = ?,
            updated_at = ?
        WHERE id = ?
          AND user_id = ?
        """,
        (
            status,
            now,
            todo_id,
            current_user.id,
        ),
    )
    
    db.commit()
    
    flash("ステータスを変更しました。", "success")
    
    return redirect(url_for("todo.index"))