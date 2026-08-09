from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length


class TodoForm(FlaskForm):
    
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルを入力してください。"),
            Length(
                max=100,
                message="タイトルは100文字以内で入力してください。"
            ),
        ],
    )
    
    description = TextAreaField(
        "詳細",
        validators=[
            Length(
                max=1000,
                message="詳細は1000文字以内で入力してください。"
            ),
        ],
    )
    
    priority = SelectField(
        "優先度",
        choices=[
            ("高", "高"),
            ("中", "中"),
            ("低", "低"),
        ],
        default="中",
    )
    
    status = SelectField(
        "状態",
        choices=[
            ("未着手", "未着手"),
            ("進行中", "進行中"),
            ("完了", "完了"),
        ],
        default="未着手",
    )
    
    deadline = DateField(
        "締切日",
        format="%Y-%m-%d",
        validators=[],
    )
    
    submit = SubmitField("更新")