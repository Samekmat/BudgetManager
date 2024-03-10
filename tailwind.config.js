module.exports = {
  darkMode: 'class',
  content: [
      './templates/**/*.html',
      './incomes/templates/incomes/*.html',
      './expenses/templates/expenses/*html',
      './users/templates/users/*html',
      './budget_manager_app/templates/budgets/*html',
      './saving_goals/templates/saving_goals/*html',
      './helper_models/templates/categories/*html',
      './helper_models/templates/tags/*html',
      './file_parsers/templates/*html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
        require('flowbite/plugin')
        ],
}
