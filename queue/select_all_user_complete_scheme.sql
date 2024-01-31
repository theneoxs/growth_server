select 
	usr1.id user_id, concat(usr1.name, ' ', usr1.surname) user_name
from
	(
SELECT distinct sb1.user_id
	FROM public.status_block sb1
	left join public.program_list pl1
	on sb1.block_id = pl1.block_id
where pl1.program_id = {prog_id} 
and sb1.block_status > '0') tt1
	left join public.user usr1
	on usr1.id = tt1.user_id