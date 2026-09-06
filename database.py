from pathlib import Path
import sqlite3


DATA_DIRECTORY = Path("data")
DATABASE_PATH = DATA_DIRECTORY / "webcafe.db"

MAX_LEVEL = 100


def initialise_database():
    """Create the database directory and required tables."""
    DATA_DIRECTORY.mkdir(exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                user_id INTEGER PRIMARY KEY,
                total_xp INTEGER NOT NULL DEFAULT 0,
                level INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS member_roles (
            user_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, role_id)
            )
            """
        )


def get_or_create_member(user_id: int):
    """Return a saved member record or create a new one."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        member = connection.execute(
            """
            SELECT user_id, total_xp, level
            FROM members
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        if member is None:
            connection.execute(
                """
                INSERT INTO members (
                    user_id,
                    total_xp,
                    level
                )
                VALUES (?, 0, 0)
                """,
                (user_id,),
            )

            member = (
                user_id,
                0,
                0,
            )

        return member


def update_member_progress(
        user_id: int,
        total_xp: int,
        level: int,
):
    """Save a member's current xp and level."""
    get_or_create_member(user_id)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            UPDATE members
            SET total_xp = ?, level = ?
            WHERE user_id = ?
            """,
            (
                total_xp,
                level,
                user_id,
            ),
        )


def save_member_roles(
    user_id: int,
    role_ids: set[int]
):
    """Save the Discord roles managed by Miso for a member."""
    get_or_create_member(user_id)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            DELETE FROM member_roles
            WHERE user_id = ?
            """,
            (user_id,),
        )

        connection.executemany(
            """
            INSERT INTO member_roles (
                user_id,
                role_id
            )
            VALUES (?, ?)
            """,
            [
                (user_id, role_id)
                for role_id in role_ids
            ],
        )


def get_member_roles(user_id: int) -> set[int]:
    """Return the saved Discord roles managed by Miso."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            """
            SELECT role_id
            FROM member_roles
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchall()

    return {
        row[0]
        for row in rows
    }


def xp_required_for_next_level(current_level: int) -> int:
    """Return the XP required to reach the next level."""
    if current_level >= MAX_LEVEL:
        return 0

    if current_level == 0:
        return 1

    return 50 + (25 * current_level)


def calculate_level(total_xp: int) -> int:
    """Calculate a member's level from their total XP."""
    level = 0
    remaining_xp = total_xp

    while level < MAX_LEVEL:
        required_xp = xp_required_for_next_level(level)

        if remaining_xp < required_xp:
            break

        remaining_xp -= required_xp
        level += 1

    return level


def add_xp(user_id: int, amount: int):
    """Add XP to a member and save their updated level."""
    member = get_or_create_member(user_id)

    old_level = member[2]
    total_xp = member[1] + amount
    new_level = calculate_level(total_xp)

    update_member_progress(
        user_id,
        total_xp,
        new_level,
    )

    return (
        total_xp,
        old_level,
        new_level,
    )


if __name__ == "__main__":
    initialise_database()