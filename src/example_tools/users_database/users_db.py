from .config import config
from verify_email import verify_email


class UsersDb:
    def __init__(self, is_credentials=True, con=None):
        if is_credentials:
            self.conn = config()
        elif con:
            self.conn = con
        else:
            raise ValueError("con parameter cannot be null if a credentials file is not provided.")
    
    def add_user(self, full_name, email):
        cur = self.conn.cursor()
        query = "insert into user_table(full_name, email) values (%s, %s) returning id"

        cur.execute(query, (full_name.lower(), email.lower()))
        result = cur.fetchone()
        user_id = result[0]
        if user_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        cur.close()

    
    def add_plot(self, name, delimitation, email):
        cur = self.conn.cursor()
        query = "insert into plot(name, delimitation, id_user) values (%s, (select st_geomfromtext(%s)), (select id from user_table where email=%s)) returning id"
        cur.execute(query, (name.lower(), delimitation, email.lower()))
        result = cur.fetchone()
        plot_id = result[0]
        if plot_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        cur.close()
    
    def add_veg_bed(self, name, delimitation, email):
        cur = self.conn.cursor()
        query = "insert into veg_bed(name, delimitation, id_user) values (%s, (select st_geomfromtext(%s)), (select id from user_table where email=%s)) returning id"
        cur.execute(query, (name.lower(), delimitation, email.lower()))
        result = cur.fetchone()
        veg_bed_id = result[0]
        if veg_bed_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        cur.close()
    
    def add_species(self, name):
        cur = self.conn.cursor()
        query = "insert into species(name) values (%s) returning id"
        cur.execute(query, (name.lower(),))
        result = cur.fetchone()
        species_id = result[0]
        if species_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        cur.close()
    
    def add_variety(self, name, species_name):
        cur = self.conn.cursor()
        query = "insert into variety(name, id_species) values (%s, (select id from species where name=%s)) returning id"
        cur.execute(query, (name.lower(), species_name.lower()))
        result = cur.fetchone()
        variety_id = result[0]
        if variety_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        cur.close()
    
    def add_plot_season(self, start_date, end_date, variety_name, plot_name, user_email):
        cur = self.conn.cursor()
        query_date = "(select cast(%s as date))"
        query_variety = "(select id from variety where name=%s)"
        query_plot = "(select plot.id from plot inner join user_table on plot.id_user=user_table.id where plot.name=%s and user_table.email=%s)"
        query = f"insert into plot_season(start_date, end_date, id_variety, id_plot) values ({query_date}, {query_date}, {query_variety},{query_plot}) returning id"
        cur.execute(query, (start_date, end_date, variety_name.lower(), plot_name.lower(), user_email.lower()))
        result = cur.fetchone()
        plot_season_id = result[0]
        if plot_season_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        
    
    def add_plant_season(self, start_date, end_date, position, variety_name, veg_bed_name, user_email):
        cur = self.conn.cursor()
        query_date = "select cast(%s as date)"
        query_variety = "select id from variety where name=%s"
        query_veg_bed = "select veg_bed.id from veg_bed inner join user_table on veg_bed.id_user=user_table.id where veg_bed.name=%s and user_table.email=%s"
        query_position = "select st_geomfromtext(%s)"
        query = f"insert into plant_season(start_date, end_date, position, id_variety, id_plot) values ({query_date}, {query_date}, {query_position}, {query_variety},{query_veg_bed}) returning id"
        cur.execute(query, (start_date, end_date, position, variety_name.lower(), veg_bed_name.lower(), user_email.lower()))
        result = cur.fetchone()
        plant_season_id = result[0]
        if plant_season_id:
            self.conn.commit()
            cur.close()
        else:
            raise ValueError('Please verify the input information.')
        
    
    def get_plot_wkt(self, name, user_email):
        cur = self.conn.cursor()
        query = "select st_astext(delimitation) from plot inner join user_table on plot.id_user=user_table.id where plot.name=%s and user_table.email=%s"
        cur.execute(query, (name, user_email.lower()))
        result = cur.fetchone()
        plot_wkt = result[0]
        if plot_wkt:
            cur.close()
            return plot_wkt
        else:
            raise ValueError('Please verify the input information.')
        
