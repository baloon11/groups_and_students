from django.db import connection
class SQL_Info(object):
    def process_response(self, request, response):
    
        sql_list=connection.queries
        len_sql_list=len(sql_list)
        total_time=float()
        for n in xrange(len_sql_list):
            total_time = total_time+ float(sql_list[n]['time'])        
        response.content = response.content.replace('</body>','<div style="padding-left:5%">'+
                                                             'number of SQL requests: '+str(len_sql_list)+ '<br>'
                                                             +'total time: '+ str(total_time)+ '</div><br></body>')
        return response
