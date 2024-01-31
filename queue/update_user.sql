update public.program_to_user as u set
	role_id = u2.role_id
from (values 
	  {data}
) as u2(program_id, user_id, role_id)
where u2.program_id = u.program_id and u2.user_id = u.user_id;