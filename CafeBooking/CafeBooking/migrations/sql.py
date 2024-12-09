from django.db import migrations

SQL = """
CREATE PROCEDURE delete_archived()
language plpgsql
AS 
$$
BEGIN
	DELETE FROM "CafeBooking_reservation" WHERE is_archivated = true;
END;
$$;

"""


class Migration(migrations.Migration):

    dependencies = [
        ("CafeBooking", "0008_setting"),
    ]

    # operations = [migrations.RunSQL(SQL)]
