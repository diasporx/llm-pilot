import re


def strip_images(text: str) -> str:
    # Удаляет inline base64-картинки вида: ![...](data:image/...;base64,...)
    text = re.sub(r"!\[[^\]]*\]\(data:image/[^)]+\)", "", text)
    # Удаляет Tracker-вставки вида: ![name.png](/ajax/v2/attachments/... =WxH)
    text = re.sub(r"!\[[^\]]*\]\(/ajax/[^)]*\)", "", text)
    return text


def serialize_issue(raw: dict, raw_comments: list) -> dict:
    def display(field):
        if field is None:
            return None
        return field.get("display") if isinstance(field, dict) else field

    comments = [
        {
            "author": display(c.get("createdBy")),
            "text": strip_images(c.get("text", "")),
            "created_at": c.get("createdAt", ""),
        }
        for c in raw_comments
        if c.get("text", "").strip()
    ]

    sprints = raw.get("sprint") or []
    sprint_name = sprints[0].get("name") if sprints else None

    return {
        "key": raw.get("key"),
        "summary": raw.get("summary"),
        "description": strip_images(raw.get("description") or ""),
        "status": display(raw.get("status")),
        "type": display(raw.get("type")),
        "priority": display(raw.get("priority")),
        "assignee": display(raw.get("assignee")),
        "author": display(raw.get("createdBy")),
        "sprint": sprint_name,
        "story_points": raw.get("storyPoints"),
        "created_at": raw.get("createdAt"),
        "updated_at": raw.get("updatedAt"),
        "resolved_at": raw.get("resolvedAt"),
        "components": [display(c) for c in (raw.get("components") or [])],
        "tags": raw.get("tags") or [],
        "comments": comments,
    }
