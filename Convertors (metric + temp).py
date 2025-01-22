'''Создал два врианта конверторов:
Для температуры: цельсий к фаренгейту и наоборот и реализовал подсчет, сколько раз им пользовались.
Для имерических и метрических значений: хороший пример использования матрицы, как табличных данных.'''


class TemperatureConvertor:
    __usages = 0

    def __usage(func):
        def wrapper(self, *args, **kwargs):
            self.__usages += 1
            result = func(*args, **kwargs)
            return result
        return wrapper

    @__usage
    @staticmethod
    def c_to_f(temp_c):
        return temp_c * 9 / 5 + 32

    @__usage
    @staticmethod
    def f_to_c(temp_f):
        return (temp_f - 32) * 5 / 9

    def show_usages(self):
        print(f"Temperature converter was used {self.__usages} time(s).")


class MetricImperialConvertor:

    @staticmethod
    def length_convertor(amount, measure_in, measure_out):
        measure = ['millimetre', 'centimetre', 'metre', 'kilometre', 'inch', 'foot', 'yard', 'mile']
        measurement_info = [[1, 0.1, 0.001, 0.000001, 5/127, 5/1524, 5/4572, 1/1609344],
                            [10, 1, 0.01, 0.00001, 50/127, 50/1524, 50/4572, 10/1609344],
                            [1000, 100, 1, 0.001, 5000/127, 1250/381, 1250/1143, 125/201168],
                            [1000000, 100000, 1000, 1, 5000000/127, 1250000/381, 1250000/1143, 15625/25146],
                            [25.4, 2.54, 0.0254, 0.0000254, 1, 1/12, 1/36, 1/63360],
                            [304.8, 30.48, 0.3048, 0.0003048, 12, 1, 1/3, 1/5280],
                            [914.4, 91.44, 0.9144, 0.0009144, 36, 3, 1, 1/1760],
                            [1609344, 160934.4, 1609.344, 1.609344, 63360, 5280, 1760, 1]]

        return amount * measurement_info[measure.index(measure_in)][measure.index(measure_out)]

    @staticmethod
    def weight_convertor(amount, measure_in, measure_out):
        metric = ['gram', 'kilogram', 'tonne']
        imperial = ['ounce', 'pound']
        measurement_info = [[28.3495, 0.02835, 0.00002835],
                            [453.592, 0.45359, 0.00045359]]
        if measure_in in metric:
            x = metric.index(measure_in)
            y = imperial.index(measure_out)
            return amount / measurement_info[y][x]
        elif measure_in in imperial:
            x = imperial.index(measure_in)
            y = metric.index(measure_out)
            return amount * measurement_info[x][y]

    @staticmethod
    def volume_convertor(amount, measure_in, measure_out):
        metric = ['litre']
        imperial = ['pint', 'gallon']
        measurement_info = [[0.568],
                            [4.546]]
        if measure_in in metric:
            x = metric.index(measure_in)
            y = imperial.index(measure_out)
            return amount / measurement_info[y][x]
        elif measure_in in imperial:
            x = imperial.index(measure_in)
            y = metric.index(measure_out)
            return amount * measurement_info[x][y]
