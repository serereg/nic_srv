class Cooler {
	constructor(id) {
	  this.id = id;
	  this.name = "ЦКТ" + id
	  this.pv = 0.0
	  this.sp = 0.0
	  this.description = "описание"
	}
  }

new Vue ({
	el: '#app',
	data: {
		N: 12,
		title: 'Hello',
		coolers: []
	},
	computed: {
		init()
		{
			for (let i = 1; i <= this.N; i++) {
				this.coolers.push(new Cooler(i))
			}
			
			return this.coolers
		}
	}
});