import os

ROOT_DIR: str = os.path.relpath(os.path.join(os.path.dirname(__file__), '..'))
PROJ_DIR: str = os.path.join(ROOT_DIR, '..')

TEST_POS_ELEC_DIR: str = os.path.join(PROJ_DIR, 'data', 'test', 'param_pos-electrode.csv')
TEST_NEG_ELEC_DIR: str = os.path.join(PROJ_DIR, 'data', 'test', 'param_neg-electrode.csv')

TEST_ELECTROLYTE_DIR: str = os.path.join(PROJ_DIR, 'data', 'test', 'param_electrolyte.csv')
TEST_ELECTROLYTE_ERROR_DIR: str = os.path.join(PROJ_DIR, 'data', 'test', 'param_electrolyte_with_errors.csv')

TEST_BATTERY_CELL_DIR: str = os.path.join(PROJ_DIR, 'data', 'test', 'param_battery-cell.csv')