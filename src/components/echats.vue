<template>
    <div id="app">
        <div id="brand-sales-rank" style="width: 600px; height: 400px;"></div>
    </div>
</template>

<script>
import echats from "echarts";
export default {
    name: 'echarts-homework',
    mounted: function () {  // mounted() 在实例挂载之后自动调用 (元素内容改变之后不会重新调用)
        var myChart = echarts.init(document.getElementById('brand-sales-rank'));
        option = {
            xAxis: {
                type: 'category',
                data: ['Matcha Latte', 'Milk Tea', 'Cheese Cocoa', 'Walnut Brownie']
            },
            yAxis: {},
            series: [
                {
                    type: 'bar',
                    name: '2015',
                    data: [89.3, 92.1, 94.4, 85.4]
                },
                {
                    type: 'bar',
                    name: '2016',
                    data: [95.8, 89.4, 91.2, 76.9]
                },
                {
                    type: 'bar',
                    name: '2017',
                    data: [97.7, 83.1, 92.5, 78.1]
                }
            ]
        };
        myChart.setOption(option);
    }
}

myChart.setOption(option);
</script>

<!-- var option = {
    dataset: {
        source: [
            ['score', 'amount', 'product'],
            [89.3, 58212, 'Matcha Latte'],
            [57.1, 78254, 'Milk Tea'],
            [74.4, 41032, 'Cheese Cocoa'],
            [50.1, 12755, 'Cheese Brownie'],
            [89.7, 20145, 'Matcha Cocoa'],
            [68.1, 79146, 'Tea'],
            [19.6, 91852, 'Orange Juice'],
            [10.6, 101852, 'Lemon Juice'],
            [32.7, 20112, 'Walnut Brownie']
        ]
    },
    xAxis: {},
    yAxis: { type: 'category' },
    series: [
        {
            type: 'bar',
            encode: {
                // 将 "amount" 列映射到 X 轴。
                x: 'amount',
                // 将 "product" 列映射到 Y 轴。
                y: 'product'
            }
        }
    ]
}; -->