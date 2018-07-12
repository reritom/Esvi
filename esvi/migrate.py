# Get DB path
# Create Migrations dir if not already existing
# Find models dir from config?
# For each model
#   Check if a migration is needed
#   Get definition from DB, if doesn't match class definition, a migration is needed
#   If names are similar, ask if they have been renamed
#   If not, add or remove
#   Run migration through adapter
#   Create migration log

# If reversal of migration, take param as version to revert to
#   Using logs to attempt reversal
