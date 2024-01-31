delete from public.tree_block
where child_id in (
select block_id
from public.program_list
where program_id = {prog_id})