class Cooler {
	constructor(id) {
	  this.id = id;
	  this.name = "ЦКТ" + id
	  this.pv = 0.0
	  this.sp = 0.0
	  this.is_reg_on = false
	  this.is_pv_fault = false
	  this.is_reg_alarm = false
	  this.description = "описание"
	}
  }

var app = new Vue ({
	el: '#app',
	data: {
		N: 12,
		coolers: [],
		cooler_control: {},
		curent_cooler_for_editing: 1, // относится к отображению
		connection_watchdog: 0,
		show_only_coolers_at_work: false
	},
	methods: {
		show_only_at_work: function () {
		  localStorage.setItem("show_busy_tank", this.show_only_coolers_at_work)
		}
	},
	computed: {
		init()
		{
			this.coolers = []
			for (let i = 1; i <= this.N; i++) {
				this.coolers.push(new Cooler(i))
			}
			
			//this.cooler_control = Object.assign({}, this.coolers[0])

			let show = localStorage.getItem("show_busy_tank")
			if (show == "true")
				this.show_only_coolers_at_work = true
			else
				this.show_only_coolers_at_work = false
			
		}
	}
});