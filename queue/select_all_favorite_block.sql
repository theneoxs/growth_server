select
    b1.id,
	b1.name,
    b1.description,
    b1.level,
    sb1.block_status
from
	public.status_block sb1
	left join public.block b1
	on sb1.block_id = b1.id
where
	sb1.user_id = '{user_id}'
	and sb1.is_favorite = True; 