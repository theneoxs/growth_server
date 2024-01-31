select
	prog1.user_id,
	concat(usr1.name, ' ', usr1.surname) user_name
from
	public.program_to_user prog1
	left join public.user usr1
	on prog1.user_id = usr1.id
where
	prog1.program_id = {program_id} and prog1.role_id = {role_id}