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
        ('CafeBooking', 'sql'),
    ]

    #operations = [migrations.RunSQL(SQL)]