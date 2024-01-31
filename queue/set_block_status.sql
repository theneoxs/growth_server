UPDATE 
    public.status_block
SET 
    block_status = {block_status}
WHERE 
    block_id = {block_id} and user_id = '{user_id}';