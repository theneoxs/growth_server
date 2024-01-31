select
	m1.block_id,
	m1.name as "block_name",
	m1.type as "block_type",
	m1.block_status,
	m1.description as "block_data",
	tb1.mother_id as "block_rel",
	null as "rel_media",
	m1.is_favorite,
	m1.level
from
	(
	select
		*
	from 
		public.program_list prog1
		left join
			(select
				bl.*,
			 	sb1.block_status,
			 	sb1.is_favorite
			from
			 	public.block bl
			left join
			 	public.status_block sb1
			on
			 	bl.id = sb1.block_id
			 	and sb1.user_id = '{user_id}'
			) bl1
		on 
			prog1.block_id = bl1.id
	where
		prog1.program_id = {program_id}
	) m1
	left join 
	public.tree_block tb1
	on m1.block_id = tb1.child_id