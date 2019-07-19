angular
  .module("app", ['ngAnimate'])
  .controller("FoodOrdersController", FoodOrdersController);

FoodOrdersController.$inject = ['$scope']
function FoodOrdersController($scope) {
  let vm = this;
  let animationTime = 500
  vm.index = 0
  vm.textAnimationName = 'slide-out'
  vm.fadeAnimationName = 'fade-in'
  vm.fadeAnimationName = 'fade-in'
  vm.takeOrder = false
  vm.availableFoods = [
    {
      name: "Birthday",
      ingredients: ["Catering", "Basic Decoration", "Hosting", "Birthday Cake"],
      extras: ['Music', 'Flower', 'Other decorations']
    },
    {
      name: "Wedding",
      ingredients: ["Host/Prayer", "Guest Arranging", "Basic Decorations", "Clothing"],
      extras: ['Flowers', "Music", "Other Decorations"]
    }
  ];
  vm.activeFood = vm.availableFoods[vm.index];

  vm.nextItem = () => {
    vm.textAnimationName = 'slide-in'
    vm.fadeAnimationName = 'fade-out'
    if(vm.index + 1 > vm.availableFoods.length - 1) {
      return
    }
    setTimeout(() => {
      vm.index++
      vm.activeFood = vm.availableFoods[vm.index];
      $scope.$apply()
    }, animationTime - 200)
  };

  vm.previousItem = () => {
    vm.textAnimationName = 'slide-out'
    vm.fadeAnimationName = 'fade-in'
    if(vm.index === 0) {
      return
    }
    setTimeout(() => {
      vm.index--
      vm.activeFood = vm.availableFoods[vm.index];
      $scope.$apply()
    }, animationTime - 200)
  };
}
