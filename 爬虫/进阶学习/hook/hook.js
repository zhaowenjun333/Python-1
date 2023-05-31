var people = {
    name: 'Bob',
};

var count = 18;

// 定义一个age 获取值时返回定义好的变量 count
Object.defineProperty(people, 'age', {
    get: function () {
        console.log('获取值！');
        return count;
    },
    set: function (val) {
        console.log('设置值！');
        count = val + 1;
    },
});

people.age = 20;
console.log(people.age);

console.log(people.age)