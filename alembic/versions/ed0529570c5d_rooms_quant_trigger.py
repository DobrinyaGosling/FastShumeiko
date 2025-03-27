from alembic import op
import sqlalchemy as sa


# Обязательные идентификаторы миграции
revision = 'ed0529570c5d'
down_revision = '3e2a1ea19553'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Удаляем колонку если существует
    op.execute("ALTER TABLE hotels DROP COLUMN IF EXISTS rooms_quantity")

    # 2. Добавляем колонку
    op.add_column(
        'hotels',
        sa.Column('rooms_quantity', sa.Integer(), nullable=False, server_default='0')
    )

    # 3. Создаём функцию-триггер
    op.execute("""
    CREATE OR REPLACE FUNCTION update_hotel_rooms_count()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            UPDATE hotels 
            SET rooms_quantity = (
                SELECT COUNT(*) FROM rooms WHERE hotel_id = OLD.hotel_id
            )
            WHERE id = OLD.hotel_id;
        ELSE
            UPDATE hotels 
            SET rooms_quantity = (
                SELECT COUNT(*) FROM rooms WHERE hotel_id = NEW.hotel_id
            )
            WHERE id = NEW.hotel_id;
        END IF;
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # 4. Вешаем триггер
    op.execute("""
    CREATE TRIGGER hotel_rooms_count_trigger
    AFTER INSERT OR UPDATE OR DELETE ON rooms
    FOR EACH ROW EXECUTE FUNCTION update_hotel_rooms_count();
    """)

    # 5. Обновляем данные
    op.execute("""
    UPDATE hotels 
    SET rooms_quantity = (SELECT COUNT(*) FROM rooms WHERE rooms.hotel_id = hotels.id);
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS hotel_rooms_count_trigger ON rooms")
    op.execute("DROP FUNCTION IF EXISTS update_hotel_rooms_count")
    op.drop_column('hotels', 'rooms_quantity')