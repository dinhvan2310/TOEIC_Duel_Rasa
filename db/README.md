# Database Cleanup Scripts for Supabase

This directory contains scripts for managing the Rasa PostgreSQL database in Supabase.

## Cleanup Old Conversations

The `cleanup_conversations.sql` script creates a scheduled task to automatically clean up old conversations and events from your Supabase database.

### What it does:
1. Deletes events older than 7 days
2. Removes conversations that have no remaining events
3. Logs cleanup activities in a dedicated `cleanup_logs` table
4. Runs automatically every day at midnight

### How to use in Supabase:

1. Go to your Supabase project dashboard
2. Click on "SQL Editor" in the left sidebar
3. Create a new query
4. Copy and paste the contents of `cleanup_conversations.sql`
5. Click "Run" to execute the script

### Checking cleanup logs:
To see the cleanup history, run this query in Supabase SQL Editor:
```sql
SELECT * FROM cleanup_logs 
ORDER BY cleanup_time DESC 
LIMIT 10;
```

### Manual cleanup:
If you need to run the cleanup manually, execute:
```sql
SELECT cleanup_old_conversations();
```

### Modifying the schedule:
To change when the cleanup runs, modify the cron schedule in the script:
```sql
-- First unschedule the existing job
SELECT cron.unschedule('cleanup-old-conversations');

-- Then schedule with new timing
SELECT cron.schedule(
    'cleanup-old-conversations',
    '0 0 * * *',  -- Change this cron expression
    $$SELECT cleanup_old_conversations()$$
);
```

Common cron schedules:
- `0 0 * * *` - Every day at midnight
- `0 */12 * * *` - Every 12 hours
- `0 0 * * 0` - Every Sunday at midnight

### Important Notes for Supabase:
1. The cleanup script uses the `pg_cron` extension which is available in Supabase
2. Cleanup logs are stored in a dedicated table for better tracking
3. The script automatically handles existing jobs to prevent duplicates
4. All timestamps are stored with timezone information 