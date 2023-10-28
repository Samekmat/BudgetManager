module.exports = {
  darkMode: 'class',
  content: [
      './templates/**/*.html',
      './incomes/templates/incomes/*.html',
      './expenses/templates/expenses/*html',
      './users/templates/users/*html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
        require('flowbite/plugin')
        ],
}
