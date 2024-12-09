from django.db import migrations

SQL = """
CREATE FUNCTION get_reservation_counter()
returns INTEGER
language plpgsql
AS
$$
declare
   counter INTEGER;
BEGIN
   SELECT count(*)
   INTO counter
   FROM "CafeBooking_reservation";
   RETURN counter;
end;
$$;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("CafeBooking", "sql2"),
    ]

    operations = [migrations.RunSQL(SQL)]
