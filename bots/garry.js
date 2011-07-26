var mongo = require('mongodb');
var sys = require('sys');

var httpAgent = require('http-agent'),
jsdom = require('jsdom'),
sys = require('sys');
var db = new mongo.Db('jobboard', new mongo.Server('localhost',27017,{}),{});

var results = new Array();
var agent = httpAgent.create('jobs.37signals.com', ['categories/1/jobs', 'categories/2/jobs','categories/3/jobs','categories/4/jobs','categories/5/jobs','categories/6/jobs','categories/7/jobs']);


 
agent.addListener('next', function (e, agent_res) {
  // Создаём DOM-дерево из текста страницы
  //for (x in agent_res){
//	sys.log(x);
  //}
  //sys.puts(agent_res.body);
  var window = jsdom.jsdom(agent_res.body).createWindow();
  // Здесь мы подключаем файл jQuery.
  jsdom.jQueryify(window, './jquery-1.4.2.min.js', function (window, jQuery) {
    // jQuery загружен и подключен к объекту window, созданному jsdom
	//sys.puts(window);
	if(jQuery('.no_results').length==0){
	  sys.puts("Category: "+jQuery('div.jobs h1 a').text());
	  jQuery('div.jobs ul li').each(function (i) {
		var job = {
		  title: jQuery(this).find('span.title').text(),
		  location: jQuery(this).find('span.city').text(),
		  company: jQuery(this).find('span.company').text(),
		  url: jQuery(this).find('a').attr('href'),
		}
		results[job['url']]=job;
		sys.puts("Job["+i+"]"+job.title+"["+job.company+"]"+" ("+job.location+") "+"{"+job.url+"}");
		sys.puts('++++++++++++++++++');
		sys.puts(job['body']);
		//sys.puts('Topic: [' + jQuery(this).find('div.comments').find('span.all').text() + '] ' + jQuery(this).find('a.topic').text());
      });
	};
	//sys.puts(jQuery('.jobs').find('h1').text());
	agent.next();
  });
});
 
agent.addListener('stop', function (agent) {
  sys.puts('the agent has stopped');
  sys.puts('ffff');
  for (x in results){
	sys.log(x);
	var job_agent =httpAgent.create('jobs.37signals.com', [x]);
	job_agent.addListener('next', function (e, job_agent_res) {
	  var job_window = jsdom.jsdom(job_agent_res.body).createWindow();
	  // Здесь мы подключаем файл jQuery.
		jsdom.jQueryify(job_window, './jquery-1.4.2.min.js', function (job_window, jQuery) {
		  if(jQuery('.no_results').length==0){
			job['body']=jQuery('.apply p').text();
			sys.puts(job['body']);
			job_agent.next();
		  }
		});
	});
	job_agent.addListener('stop', function(job_agent) {
	  sys.puts('the page agent has stopped');
	});
	
	// Запускаем спайдер2
	job_agent.start();
  }
});
 
// Запускаем спайдер
agent.start();


db.open(function(err, db){
  db.collection('jobs',function(err,collection){
	collection.find({},function(err,cursor){
	  cursor.each(function(err, item) {
		if(item!=null){
		  sys.puts(item.title);
		}
		else{
		  db.close();
		}
	  });
	});
  });
});